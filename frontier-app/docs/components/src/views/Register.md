# Register

## Expose

### username

> 用户名输入框的值 <br/>`@member` {import('vue').Ref&lt;string&gt;}

### email

> 邮箱输入框的值 <br/>`@member` {import('vue').Ref&lt;string&gt;}

### password

> 密码输入框的值 <br/>`@member` {import('vue').Ref&lt;string&gt;}

### confirmPassword

> 确认密码输入框的值 <br/>`@member` {import('vue').Ref&lt;string&gt;}

### loading

> 注册请求的加载状态 <br/>`@member` {import('vue').Ref&lt;boolean&gt;}

### register

> 提交注册请求的方法 <br/>`@function` true<br/>`@async` true<br/>`@description` 验证表单后提交注册请求，成功则跳转登录页<br/>`@throws` 注册失败时抛出错误

### goToLogin

> 跳转到登录页面的方法 <br/>`@function` true<br/>`@description` 导航到/login 路由

---

```vue live
<Register />
```
