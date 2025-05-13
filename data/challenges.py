import random
from datetime import datetime, timedelta

# 自定义参数
num_users = 10  # 用户数量
records_per_user = 30  # 每个用户参与的挑战数量
start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 1, 31)
output_file = "user_challenges.sql"  # 输出文件路径

# 计算日期范围内的天数
days_range = (end_date - start_date).days

# 定义挑战数据：(challenge_id, challenge_type, target_value)
# 根据您提供的 challenges 表数据，提取 challenge_id, type 和 target_value
challenges_data = [
    (1, 'distance', 60.0), (2, 'calories', 2500.0), (3, 'workouts', 4.0), (4, 'duration', 45.0), (5, 'distance', 200.0),
    (6, 'distance', 50.0), (7, 'calories', 3000.0), (8, 'workouts', 3.0), (9, 'duration', 60.0), (10, 'distance', 150.0),
    (11, 'distance', 70.0), (12, 'calories', 2000.0), (13, 'workouts', 5.0), (14, 'duration', 30.0), (15, 'distance', 250.0),
    (16, 'distance', 55.0), (17, 'calories', 3500.0), (18, 'workouts', 4.0), (19, 'duration', 45.0), (20, 'distance', 180.0),
    (21, 'distance', 65.0), (22, 'calories', 4000.0), (23, 'workouts', 3.0), (24, 'duration', 60.0), (25, 'distance', 220.0),
    (26, 'distance', 45.0), (27, 'calories', 1500.0), (28, 'workouts', 5.0), (29, 'duration', 30.0), (30, 'distance', 160.0),
    (31, 'distance', 75.0), (32, 'calories', 4500.0), (33, 'workouts', 4.0), (34, 'duration', 60.0), (35, 'distance', 280.0),
    (36, 'distance', 40.0), (37, 'calories', 2000.0), (38, 'workouts', 3.0), (39, 'duration', 45.0), (40, 'distance', 190.0),
    (41, 'distance', 80.0), (42, 'calories', 5000.0), (43, 'workouts', 5.0), (44, 'duration', 60.0), (45, 'distance', 300.0),
    (46, 'distance', 50.0), (47, 'calories', 2500.0), (48, 'workouts', 4.0), (49, 'duration', 30.0), (50, 'distance', 210.0)
]

# 根据挑战类型定义 current_value 的范围比例（相对于 target_value）
value_ranges = {
    'distance': (0.0, 1.2),  # 0% 到 120% 的目标值
    'calories': (0.0, 1.2),  # 0% 到 120% 的目标值
    'workouts': (0.0, 1.5),  # 0% 到 150% 的目标值（允许超额完成）
    'duration': (0.0, 1.3)   # 0% 到 130% 的目标值
}

# 生成SQL插入语句
sql_statements = []
sql_statements.append("INSERT INTO user_challenges (user_id, challenge_id, join_date, current_value, completed) VALUES")

# 存储所有用户的记录
all_records = []

for user_id in range(1, num_users + 1):
    user_records = []
    # 为每个用户生成指定数量的记录，确保覆盖多个挑战ID范围
    used_challenge_ids = set()  # 避免重复挑战ID
    target_count = records_per_user
    
    # 随机选择挑战ID，确保不重复
    challenge_ids = list(range(1, 51))  # 挑战ID从1到50
    random.shuffle(challenge_ids)
    selected_ids = challenge_ids[:target_count]
    
    for challenge_id in selected_ids:
        if challenge_id in used_challenge_ids:
            continue
        used_challenge_ids.add(challenge_id)
        
        # 获取挑战类型和目标值
        challenge_info = next(c for c in challenges_data if c[0] == challenge_id)
        challenge_type = challenge_info[1]
        target_value = challenge_info[2]
        
        # 随机生成加入日期（在2025-2026范围内）
        random_day = random.randint(0, days_range)
        join_date = start_date + timedelta(days=random_day)
        join_hour = random.randint(8, 16)
        join_minute = random.randint(0, 59)
        join_date = join_date.replace(hour=join_hour, minute=join_minute, second=0)
        join_date_str = join_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # 随机生成当前值（基于目标值和类型范围）
        range_ratio = value_ranges[challenge_type]
        current_value = round(target_value * random.uniform(range_ratio[0], range_ratio[1]), 1)
        
        # 完成状态：如果当前值大于或等于目标值，则完成，否则未完成
        completed = current_value >= target_value

        
        # 构建记录
        record = f"({user_id}, {challenge_id}, '{join_date_str}', {current_value}, {str(completed).upper()})"
        user_records.append(record)
    
    # 按join_date排序，确保时间顺序
    user_records.sort(key=lambda x: datetime.strptime(x.split("'")[1], '%Y-%m-%d %H:%M:%S'))
    
    # 添加用户注释
    sql_statements.append(f"-- 用户{user_id}（{len(user_records)}条）")
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
