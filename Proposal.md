# 软件工程Spring1 



## 一、小组成员

| 学号     | 姓名   |
| -------- | ------ |
| 12211925 | 笃岳霖 |
| 12211401 | 石岩松 |
| 12110624 | 王天瑞 |
| 12212727 | 赵欣瞳 |
| 12211806 | 舒飏   |



## 二、初步需求分析

在本次Project中，我们选择的项目为**项目1：个人健康助手**



### 1. 功能性需求分析：

​	在保持健康的过程中，规律锻炼、科学训练和持续跟踪身体状况至关重要。然而，许多人在制定健身计划、保持动力以及管理个人健康数据方面面临挑战。此外，大多数健身类应用缺乏社交互动，使得用户难以长期坚持训练。

​	本项目旨在开发一款集成健康管理的应用程序，帮助用户高效规划训练计划，同时通过社交互动增强健身动力，并参与竞技挑战，提升用户的参与感和体验。我们的核心功能包含以下几个方面：

**训练计划管理**

- 允许用户创建、编辑和安排每日或每周的锻炼任务。
- 用户可以设定个性化目标，实时追踪健身进度，并接收训练提醒，以确保按计划执行。

**健身课程预约**

- 提供在线预约功能，用户可以直接在平台上预订健身课程或场馆资源。
- 系统根据用户的偏好，展示可选的健身房或训练中心，并提供可用时间段以便快速预订。

**训练数据统计面板**

- 直观呈现用户的运动数据，包括消耗的卡路里、运动时长及训练趋势等信息。
- 通过数据分析，帮助用户了解自身的进步情况，并优化未来的训练安排。

**线上挑战与竞技**

- 允许用户加入在线健身挑战，和朋友或其他用户在特定的运动项目、目标或训练表现上进行比拼。
- 通过竞技机制，提高用户的运动积极性，并增强社区互动感。

**社交互动与排行榜**

- 用户可以添加好友，分享自己的训练成果、健身里程碑或运动心得，与朋友互动交流。
- 设有排行榜功能，展示好友或全体用户的训练进度，激发用户的竞争意识，提升健身动力。



### 2. 非功能性需求分析：

为了确保应用程序的可靠性、稳定性和用户体验，我们对以下这几个方面的**非功能性需求**进行了分析：



**1. 可用性（Usability）**

**目标**：确保应用易于使用，提供良好的用户体验，提高用户粘性。

-   **直观的用户界面**：设计简洁清晰的 UI，易于用户导航和操作。
-   **操作便捷性**：减少用户输入成本，如提供自动填充、语音识别等功能。
-   **训练提醒与反馈**：通过推送通知、日程提醒等方式，帮助用户保持健身计划的执行。

------

**2. 可靠性（Reliability）**

**目标**：确保系统稳定运行，不因故障导致数据丢失或应用崩溃。

-   **高可用架构**：采用负载均衡、CDN、云存储等技术，确保系统高可用性。
-   **错误处理机制**：对于崩溃、网络故障等情况，提供自动恢复或友好的错误提示。
-   **定期数据备份**：防止因服务器故障导致用户数据丢失，支持云端备份与恢复。
-   **离线模式支持**：允许用户在无网络时仍能访问训练计划，并在联网后同步数据。

------

**3. 性能（Performance）**

**目标**：确保应用响应迅速，提供流畅的用户体验，特别是在数据统计和社交互动方面。

-   **快速响应**：优化数据库查询、采用缓存（如 Redis），减少加载时间。
-   **高并发处理**：支持多人在线使用，避免因流量高峰导致系统卡顿或崩溃。
-   **数据同步优化**：确保训练记录、排行榜等数据的实时更新，同时减少对服务器的压力。

------

**4. 安全性（Security）**

**目标**：保护用户的个人信息和训练数据，防止未授权访问。

-   **身份验证机制**：采用加密认证等方式确保账户安全。
-   **数据加密**：对用户的健康数据、训练记录等敏感信息进行加密存储（如 AES-256）。
-   **防止SQL注入/XSS攻击**：使用参数化查询，防止恶意代码攻击。
-   **访问权限控制**：确保不同用户角色（普通用户、教练、管理员）只能访问相应的功能。

------

**5. 隐私保护（Confidentiality & Privacy）**

**目标**：保护用户的隐私，遵守数据保护法规。

-   **用户数据自主权**：允许用户查看、导出或删除自己的数据。
-   **最小数据存储**：仅收集必要的数据，不存储敏感信息（如生物识别数据）除非必要。
-   **匿名化处理**：排行榜、社交分享等功能可支持匿名模式，防止个人信息泄露。
-   **隐私政策透明度**：提供清晰的隐私声明，说明数据如何使用、共享及保护。



### 3. 数据需求：

**1. 关键数据类别**

系统需要管理和处理的数据主要包括以下几类：

| **数据类型**          | **数据示例**                                           | **用途**                 |
| --------------------- | ------------------------------------------------------ | ------------------------ |
| **用户信息**          | 用户名、性别、年龄、身高、体重、邮箱、头像             | 账户管理、个性化推荐     |
| **训练计划数据**      | 训练类型（跑步、瑜伽、力量训练等）、训练时长、目标设定 | 训练任务管理、进度追踪   |
| **训练记录数据**      | 训练完成时间、消耗卡路里、心率变化、步数、运动距离     | 训练数据可视化、用户反馈 |
| **健康数据**          | 心率、血氧、睡眠质量、步数、活动时间                   | 运动健康分析、智能建议   |
| **预约数据**          | 预约的课程/场馆、时间、教练信息                        | 健身课程预约             |
| **社交互动数据**      | 朋友圈动态、点赞、评论                                 | 社交分享                 |
| **挑战 & 排行榜数据** | 竞赛参与者、挑战成绩、排行榜排名                       | 竞技激励                 |
| **设备数据**          | 设备型号、系统版本、地理位置                           | 兼容性优化、用户体验改进 |



**2. 数据来源及获取方式**

数据可以通过用户输入、传感器、API 或第三方数据平台进行采集。以下是具体的数据获取方式：

| **数据来源**          | **获取方式**                     | **示例**                     |
| --------------------- | -------------------------------- | ---------------------------- |
| **用户输入**          | 用户手动填写                     | 个人信息、训练目标、饮食记录 |
| **移动设备传感器**    | 手机加速度计、GPS、心率传感器    | 记录步数、跑步距离、实时心率 |
| **系统自动计算**      | 根据训练时长、体重、运动类型计算 | 计算卡路里消耗、运动强度     |
| **健身房 & 训练机构** | 第三方API 或内部数据库           | 课程信息、预约时间           |
| **社交互动**          | 用户互动记录                     | 评论、点赞、排行榜数据       |
| **公开数据**          | 运动指南、健康建议API            | 健康知识、训练建议           |



**3. 数据处理与分析**

收集的数据不仅用于存储，还需要进行分析，以提供智能反馈和优化用户体验。

 **数据分析应用场景**：

- **个性化训练建议**
  - 通过机器学习分析用户的训练数据，提供**个性化健身计划**（如调整训练强度、推荐新运动）。
- **健康趋势分析**
  - 结合心率、步数、睡眠数据，提供**健康趋势报告**（如睡眠质量如何影响训练表现）。
- **用户激励策略**
  - 统计用户的运动数据，生成排行榜，提高用户参与度。
- **AI 训练优化**
  - 通过用户的过往数据预测最佳训练计划，如**何时进行高强度训练、何时休息**。



**5. 数据隐私与安全**

由于涉及健康数据，必须确保数据安全和合规：

 **数据安全策略**

- **加密存储**：使用 **AES-256** 加密敏感数据，如用户个人信息、健康数据。
- **数据传输加密**：保护数据在传输过程中不被窃取。
- **访问控制**：不同用户角色（普通用户、教练、管理员）只能访问相应数据。
- **数据匿名化**：排行榜、社交互动等敏感数据可采用**匿名显示**，避免隐私泄露。
- **法规合规**：符合隐私保护法规，确保用户数据安全。



### 4. 技术需求：

- 前端：Vue3为主要框架，用axios与后端API链接
- 后端：基于FastAPI框架以及Python构建后端服务器
- 数据库：Mysql



## 三、任务分解与规划

见Github-Product，已上传



## 四、AI使用情况

见腾讯问卷，已提交

