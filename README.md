# My First Taste of AI Agents

> OpenAI Agent SDK: https://openai.github.io/openai-agents-python/
>
> OpenAI Agent Github: https://github.com/openai/openai-agents-python/blob/main/docs/quickstart.md
>
> OpenAI API 管理介面: https://platform.openai.com/traces
>
> Google Customer Search API Dashboard: https://console.cloud.google.com/apis/api/customsearch.googleapis.com/quotas?inv=1&invt=AbsbYg&project=ai-web-search-1742221607831
>
>  程式化搜尋引擎 管理介面： https://programmablesearchengine.google.com/controlpanel/overview?cx=57da8c5fd28264b89

Folder structure:

```
my_agent_project/
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

## old version
ai_agent_test/
    .venv # after create venv
    src/__init__.py
    src/my_basic_agent.py
    src/handoff_routing.py
    src/add_guardrail.py
    src/Agents_as_tools.py
    src/basic_web_search.py
    src/custom_web_search.py
    ...
    README.md
    requirements.txt
    .env # create by yuor own

```

## setup venv

```
$ python -m venv .venv

$ source .venv/bin/activate

$ pip install --upgrade pip

$ pip install -r requirements.txt

```

## Prepare `.env` file to keep your API KEY

    - Apply and create API KEY from [OpenAI Plateform](https://platform.openai.com/settings/organization/api-keys)

## 1. Create my first basic agent

> ref: https://openai.github.io/openai-agents-python/

## 2. Handoff routing

## 3. Guardrails

## 4. Agents as tool

## 5. Web Search Tool

## 6. parallelization: 一個 AI 被呼叫多次，再由另一個 AI 挑選最好的答案

## 7. deterministic: 一個 AI 產出結果，另一個 AI 負責判斷