"""
This example demonstrates a deterministic flow, where each step is performed by an agent.
1. The first agent classfy the user input is related to spanding or not
2. If the user input is not related to spending, we stop here (with Input Guardrail check)
3. If the user input is related to spending, we feed the user input into the second agent

4. The second agent check the user input be able to using 3 types of SQL (SQL_1 to SQL_3) to get the answer or not
5. If the user input is not able to using 3 types of SQL to get the answer, we stop here (with Output Guardrail 1 check)
6. If the user input is able to using 3 types of SQL to get the answer, we feed the user input into the third agent

7. The third agent fill-in the info from user input using 3 types of SQL to generate the SQL query (provide the tables' schema)

8. The fourth agent check the SQL query is able to get the answer or not 
    (run the SQL query using pandas' .query() to check the answer)
9. If the SQL query is not able to get the answer, we stop here (with Output Guardrail 2 check)
10. If the SQL query is able to get the answer, we feed the SQL query into the fifth agent

11. The fifth agent summarize the SQL result and provide the final output
12. The final output is the query result with summary.

The agents are:
- Input Guardrail check
- Output Guardrail 1 check
- Output Guardrail 2 check
- Agent_1_classify: Classify the user input is related to crited card spanding or not
- Agent_2_check_SQL: Check the user input be able to using few specific SQL to get the answer or not
- Agent_3_fillin_info: Fill-in the info from user input
- Agent_4_run_SQL: Run the SQL query using pandas' .query() to get the answer
- Agent_5_generate_SQL: Summarize the query result and provide the final output.

Three types of SQL: 
- SQL_1: SELECT top({N}) FROM table WHERE customer_id = {value} AND date between {value} and {value} and spand_type = {value}
- SQL_2: SELECT store, item, spand_type, amount FROM table WHERE customer_id = {value} AND date between {value} and {value} and amount > {value}
- SQL_3: SELECT store, item, spand_type, amount FROM table WHERE customer_id = {value} AND date between {value} and {value} and store = {value}


ai_agent_project/
│
├── main.py                  # 執行入口
├── context.py               # 定義 CustomContext
│
├── agents/
│   ├── __init__.py
│   ├── agent_classify.py    # 第一個 agent
│   ├── agent_query.py       # 第二個 agent
│
├── tools/
│   ├── __init__.py
│   ├── spending_tool.py     # 消費紀錄 Tool
│   ├── other_tool.py        # 其他 Tool
│
└── models/
    ├── __init__.py
    └── schema.py            # 定義 pydantic schema
"""
import os
import pandas as pd
from typing import Any
from pydantic import BaseModel
from agents import Agent, Runner
from agents import RunContextWrapper, FunctionTool
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agents import set_default_openai_key
from dotenv import load_dotenv

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)

# --------------------------
# Part 1: 生成資料 CSV
# --------------------------
# -> src/utils/generate_user_spanding.py
# 模擬資料

# df = pd.read_csv(csv_file)

# --------------------------
# Part 2: 定義 Tool - spending_tool
# --------------------------
class CustomContext:
    def __init__(self, csv_path: str, customer: str):
        self.csv_path = csv_path
        self.customer = customer


class CustomerArgs(BaseModel):
    username: str

    class Config:
        extra = "forbid"  # pydantic 會自動加入 additionalProperties=False


async def query_spending(ctx: RunContextWrapper[CustomContext], args: str) -> str:
    csv_path = ctx.context.csv_path
    customer = ctx.context.customer

    df = pd.read_csv(csv_path)
    df_filtered = df[df['customer'] == customer]

    if df_filtered.empty:
        return f"找不到 {customer} 的任何消費紀錄。"
    return f"有 {customer} 的消費紀錄。"


spending_tool = FunctionTool(
    name="query_spending_tool",
    description="查詢是否有使用者消費紀錄",
    params_json_schema=CustomerArgs.model_json_schema(),
    on_invoke_tool=query_spending
)

# --------------------------
# Agent_1_classify: Classify the user input is related to crited card spanding or not
# --------------------------
class Agent_1_Output(BaseModel):
    '''
    This is the Agent_1_classify's output type.
    '''
    is_spanding_question: bool
    reasoning: str

classfiy_agent = Agent(
    model="gpt-4o-mini",
    name="1_classfiy_agent",
    instructions="You classify the user input is related to their own spanding or not?",
    output_type=Agent_1_Output,
    tools=[
        spending_tool,
    ],
)

# --------------------------

async def main():
    # 模擬使用者
    import random

    csv_file = "customer_spending.csv"
    customers = ["陳小姐", "張先生", "王小姐"]
    user = random.choice(customers)
    print(f"Customers: {user}")
    # 建立 context 帶入 user 資訊（模擬用）
    context = CustomContext(csv_path=csv_file, customer=user)
    result = await Runner.run(classfiy_agent, input="what is my spending in the last month?", context=context)
    print(result.final_output)
    # try:
    #     result = await Runner.run(classfiy_agent, input="what is my spending in the last month?")
    #     print(result.final_output)
    # except InputGuardrailTripwireTriggered:
    #     print(">>> Input guardrail tripped! It's not translation task.")
    # except OutputGuardrailTripwireTriggered:
    #     print(">>> Output guardrail tripped! The output is too long.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())