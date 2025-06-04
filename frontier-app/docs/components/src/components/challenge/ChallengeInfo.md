# ChallengeInfo

## Props

| Prop name   | Description | Type      | Values | Default |
| ----------- | ----------- | --------- | ------ | ------- |
| challengeId |             | undefined | -      |         |

## Expose

### challenge

> 挑战详情数据 <br/>`@member` {import('vue').Reactive&lt;Object&gt;}

### challengeInfo

> 处理后的挑战信息 <br/>`@member` {import('vue').Reactive&lt;{data: Object}&gt;}

### participants

> 参与者的分组数据 <br/>`@member` {import('vue').Reactive&lt;{pairs: Array}&gt;}

### isJoined

> 当前用户是否已加入挑战 <br/>`@member` {import('vue').Ref&lt;boolean&gt;}

### isEnd

> 挑战是否已结束 <br/>`@member` {import('vue').ComputedRef&lt;boolean&gt;}

### update

> 更新挑战进度 <br/>`@function` true<br/>`@param` 新的进度值

### endChallenge

> 结束当前挑战 <br/>`@function` true

### joinChallenge

> 加入当前挑战 <br/>`@function` true

### isMine

> 检查是否是当前用户创建的挑战 <br/>`@function` true<br/>`@param` 用户 ID<br/>`@returns` undefined

---

```vue live
<ChallengeInfo />
```
