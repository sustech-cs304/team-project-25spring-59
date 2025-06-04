# Challenge

## Expose

### userId

> 当前用户 ID <br/>`@member` {string}<br/>`@description` 可用于父组件设置或获取当前用户<br/>`@example` // 父组件中设置用户 ID<br/>challengeViewRef.value.userId = 'user123';

### challengeId

> 当前查看的挑战 ID <br/>`@member` {string}<br/>`@description` 当前正在查看的挑战任务 ID<br/>`@example` // 父组件获取当前挑战 ID<br/>const currentId = challengeViewRef.value.challengeId;

### goToChallenge

> 跳转到指定挑战详情 <br/>`@function` true<br/>`@param` 挑战任务 ID<br/>`@description` 供父组件直接跳转到指定挑战详情页<br/>`@example` // 父组件跳转到挑战详情<br/>challengeViewRef.value.goToChallenge('12345');

### goToList

> 刷新挑战列表 <br/>`@function` true<br/>`@description` 返回列表页并触发数据刷新<br/>`@example` // 父组件刷新列表<br/>challengeViewRef.value.goToList();

---

```vue live
<Challenge />
```
