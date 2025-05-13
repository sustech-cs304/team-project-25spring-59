import random
from datetime import datetime, timedelta
import json

# 定义活动类型和对应的数据范围
activity_types = [
    ("Running", {"duration": (30, 120), "distance": (3.0, 10.0), "calories": (200, 500), "avg_hr": (120, 150), "max_hr": (150, 180)}),
    ("Cycling", {"duration": (45, 180), "distance": (10.0, 30.0), "calories": (300, 700), "avg_hr": (110, 140), "max_hr": (140, 170)}),
    ("Swimming", {"duration": (30, 90), "distance": (0.5, 2.5), "calories": (150, 300), "avg_hr": (100, 130), "max_hr": (130, 160)}),
    ("Yoga", {"duration": (45, 90), "distance": None, "calories": (100, 200), "avg_hr": (80, 100), "max_hr": (100, 120)}),
    ("Strength Training", {"duration": (45, 120), "distance": None, "calories": (180, 300), "avg_hr": (110, 140), "max_hr": (140, 170)})
]

# 自定义参数
num_users = 10  # 用户数量
records_per_user = 2000  # 每个用户的记录条数
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
output_file = "training_records.sql"  # 输出文件路径

# 计算日期范围内的天数
days_range = (end_date - start_date).days

# 辅助函数：生成随机的分钟心率数据，与duration_minutes分钟数一致
def generate_minute_heart_rates(avg_hr, duration):
    heart_rates = {}
    # 为每一分钟生成一个心率值，围绕平均心率波动
    for i in range(1, duration + 1):
        heart_rates[str(i)] = random.randint(max(60, avg_hr - 10), min(avg_hr + 10, 180))
    return json.dumps(heart_rates)

# 生成SQL插入语句
sql_statements = []
sql_statements.append("INSERT INTO training_records (user_id, start_time, end_time, activity_type, duration_minutes, is_completed, record_type, reminder_time, distance, calories, average_heart_rate, max_heart_rate, minute_heart_rates) VALUES")

# 存储所有用户的记录
all_records = []
for user_id in range(1, num_users + 1):
    user_records = []
    # 为每个用户生成指定数量的记录
    for _ in range(records_per_user):
        # 随机选择一个活动类型
        activity, data_ranges = random.choice(activity_types)
        
        # 随机生成开始日期（在2025年范围内均匀分布）
        random_day = random.randint(0, days_range)
        start_time = start_date + timedelta(days=random_day)
        # 随机生成一天中的开始时间（7:00到20:00之间）
        start_hour = random.randint(7, 20)
        start_minute = random.randint(0, 59)
        start_time = start_time.replace(hour=start_hour, minute=start_minute, second=0)
        
        # 计算持续时间和结束时间
        duration = random.randint(data_ranges["duration"][0], data_ranges["duration"][1])
        end_time = start_time + timedelta(minutes=duration)
        
        # 提醒时间为开始时间前10分钟
        reminder_time = start_time - timedelta(minutes=10)
        
        # 生成其他数据
        distance = round(random.uniform(data_ranges["distance"][0], data_ranges["distance"][1]), 1) if data_ranges["distance"] else "NULL"
        calories = random.randint(data_ranges["calories"][0], data_ranges["calories"][1])
        avg_hr = random.randint(data_ranges["avg_hr"][0], data_ranges["avg_hr"][1])
        max_hr = random.randint(data_ranges["max_hr"][0], data_ranges["max_hr"][1])
        minute_hr = generate_minute_heart_rates(avg_hr, duration)
        is_completed = random.choice([True, False])
        
        # 格式化时间字符串
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        reminder_time_str = reminder_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # 构建记录
        record = f"({user_id}, '{start_time_str}', '{end_time_str}', '{activity}', {duration}, {str(is_completed).lower()}, 'record', '{reminder_time_str}', {distance}, {calories}, {avg_hr}, {max_hr}, '{minute_hr}')"
        user_records.append(record)
    
    # 按start_time排序，确保时间顺序
    user_records.sort(key=lambda x: datetime.strptime(x.split("'")[1], '%Y-%m-%d %H:%M:%S'))
    
    # 添加用户注释
    sql_statements.append(f"-- 用户{user_id}（{records_per_user}条）")
    # 将用户记录添加到总记录中
    all_records.extend(user_records)

# 将所有记录添加到SQL语句中，并处理逗号和分号
for i, record in enumerate(all_records):
    if i < len(all_records) - 1:
        sql_statements.append(record + ",")
    else:
        sql_statements.append(record + ";")

# 将SQL语句写入文件
with open(output_file, 'w', encoding='utf-8') as f:
    for statement in sql_statements:
        f.write(statement + "\n")

print(f"SQL statements have been saved to {output_file}")
