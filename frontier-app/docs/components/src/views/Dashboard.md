# Dashboard

## Expose

### records

> 原始训练记录数据 <br/>`@member` {Array&lt;{date: string, type: string, duration: number, calories: number}&gt;}<br/>`@description` 包含所有训练记录的数组，每个记录包含日期、类型、时长和卡路里<br/>`@example` // 父组件中获取原始数据<br/>const rawData = dashboardRef.value.records;

### totalDuration

> 总训练时长（分钟） <br/>`@member` {number}<br/>`@description` 计算所有训练记录的总时长（单位：分钟）<br/>`@example` // 父组件中获取总时长<br/>const minutes = dashboardRef.value.totalDuration;

### totalCalories

> 总消耗卡路里 <br/>`@member` {number}<br/>`@description` 计算所有训练记录的总卡路里消耗<br/>`@example` // 父组件中获取总卡路里<br/>const cals = dashboardRef.value.totalCalories;

### totalSessions

> 总训练次数 <br/>`@member` {number}<br/>`@description` 训练记录的总数量<br/>`@example` // 父组件中获取训练次数<br/>const sessions = dashboardRef.value.totalSessions;

### goalProgress

> 目标进度百分比 <br/>`@member` {number}<br/>`@description` 当前训练时长与目标时长的百分比（上限 100%）<br/>`@example` // 父组件中获取进度<br/>const progress = dashboardRef.value.goalProgress;

### filteredRecords

> 根据日期筛选后的记录 <br/>`@member` {Array}<br/>`@description` 基于 selectedDate 范围筛选后的训练记录<br/>`@example` // 父组件中设置日期范围<br/>dashboardRef.value.selectedDate = [new Date('2023-01-01'), new Date('2023-12-31')];<br/>// 然后获取筛选结果<br/>const filtered = dashboardRef.value.filteredRecords;

### chartData

> 折线图数据 <br/>`@member` {Object}<br/>`@property` 图表数据集<br/>`@description` 用于 LineChart 组件的格式化数据<br/>`@example` // 父组件中获取图表数据<br/>const lineData = dashboardRef.value.chartData;

### pieData

> 饼图数据 <br/>`@member` {Object}<br/>`@property` 图表数据集<br/>`@description` 用于 PieChart 组件的格式化数据<br/>`@example` // 父组件中获取饼图数据<br/>const pieData = dashboardRef.value.pieData;

### fetchTrainingData

> 重新加载训练数据 <br/>`@function` true<br/>`@async` true<br/>`@description` 强制刷新所有统计数据和图表<br/>`@example` // 父组件中刷新数据<br/>await dashboardRef.value.fetchTrainingData();

### selectedDate

> 当前选择的日期范围 <br/>`@member` {[Date, Date]\|null}<br/>`@description` 用于筛选的双日期范围（开始日期和结束日期）<br/>`@example` // 父组件中设置日期范围<br/>dashboardRef.value.selectedDate = [new Date(), new Date()];

---

```vue live
<Dashboard />
```
