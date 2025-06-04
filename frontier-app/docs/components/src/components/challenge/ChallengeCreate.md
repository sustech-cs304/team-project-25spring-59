# ChallengeCreate

## Events

| Event name | Properties | Description |
| ---------- | ---------- | ----------- |
| backToList |            |

## Expose

### form

> 表单数据对象 <br/>`@member` {import('vue').Reactive&lt;{<br/> title: string,<br/> description: string,<br/> start_date: string,<br/> end_date: string,<br/> challenge_type: string,<br/> target_value: string,<br/> created_by: number<br/>}&gt;}

### submit

> 提交表单数据 <br/>`@function` true<br/>`@async` true<br/>`@returns` undefined<br/>`@description` 提交挑战表单数据到服务器，成功后显示成功消息并刷新页面

---

```vue live
<ChallengeCreate />
```
