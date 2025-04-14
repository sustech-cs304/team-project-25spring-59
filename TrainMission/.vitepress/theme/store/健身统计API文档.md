# 健身统计API文档

本API提供用于获取用户健身训练统计数据的接口，包括训练总结和每周趋势。所有接口使用JSON格式的请求和响应体。

## 基础URL
`http://localhost:8000`

## 接口列表

### 1. 获取训练总结 (/stats/summary)

#### 请求
- **方法**：POST  
- **URL**：`/stats/summary`  
- **Content-Type**：`application/json`  

#### 请求参数
```json
{
  "user_id": "integer"
}
```
- **user_id**（必填）：用户的唯一标识符，类型为整数。

#### 响应
- **状态码**：200 OK  
- **Content-Type**：`application/json`

```json
{
  "total_minutes": "integer",
  "estimated_calories": "float",
  "actual_calories": "integer",
  "average_heart_rate": "integer",
  "max_heart_rate": "integer"
}
```

#### 响应字段说明
- **total_minutes**：所有训练记录的总时长（单位：分钟）。  
- **estimated_calories**：基于MET值（假设为8）和用户体重估算的总卡路里消耗（单位：千卡）。  
- **actual_calories**：根据训练记录中的卡路里消耗字段汇总计算出的实际卡路里（单位：千卡）。  
- **average_heart_rate**：所有记录中的平均心率（单位：bpm）。如果有多条记录，则计算平均值。  
- **max_heart_rate**：所有记录中的最大心率（单位：bpm）。

#### 错误处理
- **404 用户不存在**：当提供的`user_id`无效或在数据库中找不到对应的用户时，返回此错误。  
  ```json
  {
    "detail": "用户不存在"
  }
  ```

#### 示例
**请求**  
```
POST http://localhost:8000/stats/summary
Content-Type: application/json

{
  "user_id": 1
}
```

**响应**  
```json
{
  "total_minutes": 450,
  "estimated_calories": 2000.0,
  "actual_calories": 1800,
  "average_heart_rate": 125,
  "max_heart_rate": 150
}
```

---

### 2. 获取训练时长趋势 (/stats/weekly-trend)

#### 请求
- **方法**：POST  
- **URL**：`/stats/weekly-trend`  
- **Content-Type**：`application/json`  

#### 请求参数
```json
{
  "user_id": "integer"
}
```
- **user_id**（必填）：用户的唯一标识符，类型为整数。

#### 响应
- **状态码**：200 OK  
- **Content-Type**：`application/json`

```json
{
  "2025-04-07": {
    "duration_minutes": "integer",
    "calories": "integer",
    "avg_heart_rate": "integer",
    "max_heart_rate": "integer"
  },
  "2025-04-08": {
    "duration_minutes": "integer",
    "calories": "integer",
    "avg_heart_rate": "integer",
    "max_heart_rate": "integer"
  }
}
```

#### 响应字段说明
- **duration_minutes**：该日期的总训练时长（单位：分钟）。  
- **calories**：该日期的总卡路里消耗（单位：千卡）。  
- **avg_heart_rate**：该日期的平均心率（单位：bpm）。如果该日期没有心率数据，则返回`null`。  
- **max_heart_rate**：该日期的最大心率（单位：bpm）。如果该日期没有心率数据，则返回`null`。

#### 错误处理
- **404 用户不存在**：当提供的`user_id`无效或在数据库中找不到对应的用户时，返回此错误。  
  ```json
  {
    "detail": "用户不存在"
  }
  ```

#### 示例
**请求**  
```
POST http://localhost:8000/stats/weekly-trend
Content-Type: application/json

{
  "user_id": 1
}
```

**响应**  
```json
{
  "2025-04-07": {
    "duration_minutes": 60,
    "calories": 500,
    "avg_heart_rate": 120,
    "max_heart_rate": 150
  },
  "2025-04-08": {
    "duration_minutes": 45,
    "calories": 400,
    "avg_heart_rate": 125,
    "max_heart_rate": 160
  }
}
```