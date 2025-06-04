# ImageDetail

## Expose

### id

> 当前图片 ID（来自路由参数） <br/>`@member` {import('vue').ComputedRef&lt;string&gt;}<br/>`@description` 从路由参数中获取的当前图片 ID（响应式计算属性）

### imageUrl

> 根据 ID 生成的图片 URL <br/>`@member` {import('vue').ComputedRef&lt;string&gt;}<br/>`@description` 基于 ID 自动生成的图片资源路径（格式：/0{id}.jpg）

### goBack

> 返回轮播图页面 <br/>`@function` true<br/>`@description` 导航回轮播图列表页面

### route

> 当前路由对象（只读） <br/>`@member` {import('vue-router').RouteLocationNormalizedLoaded}<br/>`@description` Vue Router 的当前路由对象<br/>`@warning` 不建议直接修改

### router

> 路由实例（只读） <br/>`@member` {import('vue-router').Router}<br/>`@description` Vue Router 实例<br/>`@warning` 谨慎操作路由跳转

---

```vue live
<ImageDetail />
```
