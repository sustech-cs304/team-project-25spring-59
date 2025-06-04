# ReservationRecord

## Expose

### userId

> 当前登录用户 ID <br/>`@description` 从 localStorage 中获取的用户唯一标识符<br/>`@member` {string}

### personalCourses

> 用户预约的课程列表 <br/>`@description` 包含用户所有预约课程信息的响应式对象，数据已按预约时间排序<br/>`@member` {import("vue").Reactive&lt;{data?: Array&lt;{<br/> id: number,<br/> courseName: string,<br/> reservationTime: string,<br/> status: string,<br/> coach: string,<br/> location: string<br/>}&gt;}&gt;}

### processData

> 处理课程数据的方法 <br/>`@description` 对获取的课程数据进行处理并按预约时间从新到旧排序<br/>`@function` true<br/>`@param` 从 API 获取的原始课程数据<br/>`@returns` undefined

### denyReservation

> 取消课程预约的方法 <br/>`@description` 向服务器发送请求取消指定课程预约，成功后刷新页面<br/>`@function` true<br/>`@param` 要取消的课程 ID<br/>`@returns` undefined

---

```vue live
<ReservationRecord />
```
