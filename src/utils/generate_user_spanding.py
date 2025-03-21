import csv
import random
from datetime import datetime, timedelta
import uuid

# customers = ["Annie", "Jack", "Tom"]
# categories = ["Dining", "Clothing", "Electronics", "Consumer Goods", "Transportation"]
# 每個 store 與對應的 items
# stores = {
#     "Dining": {
#         "McDonald's": ["fries", "hamburger", "Coca Cola"],
#         "Starbucks": ["Coffee", "Lemonade", "Hot Chocolate"],
#         "KFC": ["Chicken Box Meal", "Chicken Sandwich", "Egg Tart"]
#     },
#     "Clothing": {
#         "H&M": ["cloth_HM1", "cloth_HM2", "cloth_HM3"],
#         "Uniqlo": ["cloth_U1", "cloth_U2", "cloth_U3"],
#         "Zara": ["cloth_Za1", "cloth_Za2", "cloth_Za3"]
#     },
#     "Electronics": {
#         "Best Buy": ["TV_BB", "Phone_BB", "Computer_BB"],
#         "Apple Store": ["iphon", "Macbook Air", "Apple Watch"],
#         "Amazon": ["ipad", "kindle", "ASUS Zenbook"]
#     },
#     "Consumer Goods": {
#         "Walmart": ["milk", "water", "toilet paper"],
#         "Costco": ["water", "toilet paper", "egg"],
#         "Target": ["toilet paper", "water", "banana"]
#     },
#     "Transportation": {
#         "Uber": ["Uber1", "Uber2", "Uber3"],
#         "Lyft": ["Lyft1", "Lyft2", "Lyft3"],
#         "Metro": ["Metro_A2B", "Metro_B2C", "Metro_B2D"]
#     }
# }


customers = ["陳小姐", "張先生", "王小姐"]
categories = ["餐飲", "服飾", "消費性電子產品", "生活用品", "交通"]
# 每個 store 與對應的 items
stores = {
    "餐飲": {
        "McDonald's": ["薯條", "勁辣雞腿堡", "可口可樂"],
        "Starbucks": ["熱美式", "拿鐵", "熱可可"],
        "KFC": ["青花驕椒麻脆雞", "義式香草紙包雞", "蛋塔"]
    },
    "服飾": {
        "H&M": ["牛仔褲", "牛仔襯衫", "裙子"],
        "Uniqlo": ["圓領短袖", "長褲", "側背包"],
        "Zara": ["大衣", "襯衫", "西裝褲"]
    },
    "消費性電子產品": {
        "Best Buy": ["電視", "手機", "電腦"],
        "Apple Store": ["iPhone", "Macbook Air", "Apple Watch"],
        "Amazon": ["音響", "kindle", "ASUS Zenbook"]
    },
    "生活用品": {
        "Walmart": ["牛奶", "水", "衛生紙"],
        "Costco": ["果汁", "衛生紙", "可頌"],
        "Target": ["衛生紙", "蛋", "香蕉"]
    },
    "交通": {
        "Uber": ["Uber1", "Uber2", "Uber3"],
        "Lyft": ["Lyft1", "Lyft2", "Lyft3"],
        "Metro": ["Metro_A2B", "Metro_B2C", "Metro_B2D"]
    }
}

rows = []

for customer in customers:
    num_records = random.randint(5, 10)
    for _ in range(num_records):
        category = random.choice(categories)
        store = random.choice(list(stores[category].keys()))
        item = random.choice(stores[category][store])
        amount = round(random.uniform(5, 500), 2)
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        trans_uuid = str(uuid.uuid4())
        rows.append({
            "customer": customer,
            "item": item,
            "store": store,
            "category": category,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "trans_uuid": trans_uuid
        })

# 儲存成 CSV
csv_file = "customer_spending_zh.csv"
with open(csv_file, "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV 檔案 {csv_file} 已成功建立")
