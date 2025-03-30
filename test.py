import re
from datetime import datetime

markdown_content = """
---
title: "🏃‍♂️ 跑步 运动记录"
date: "2025-03-19T14:21:37.471Z"
---
## 运动详情
- ​**开始时间**: 2025-03-04T22:21
- ​**结束时间**: 2025-04-05T22:21
- ​**运动类型**: 跑步
- ​**时长**: 46080 分钟
"""

# 提取开始时间
start_time_match = re.search(r"开始时间\*\*:\s*([^\n]+)", markdown_content)
start_time = datetime.fromisoformat(start_time_match.group(1)) if start_time_match else None

# 提取结束时间
end_time_match = re.search(r"结束时间\*\*:\s*([^\n]+)", markdown_content)
end_time = datetime.fromisoformat(end_time_match.group(1)) if end_time_match else None

# 提取运动类型（去除表情符号）
activity_type_match = re.search(r"运动类型\*\*:\s*([^\n]+)", markdown_content)
activity_type = activity_type_match.group(1) if activity_type_match else None

# 提取时长（分钟）
duration_match = re.search(r"时长\*\*:\s*(\d+)", markdown_content)
duration_minutes = int(duration_match.group(1)) if duration_match else None

# 结果
result = {
    "start_time": start_time,
    "end_time": end_time,
    "activity_type": activity_type,
    "duration_minutes": duration_minutes
}

print(result)