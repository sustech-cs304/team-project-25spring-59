# Login

## Expose

### username

> 当前输入的用户名 <br/>`@member` {import('vue').Ref&lt;string&gt;}

### password

> 当前输入的密码 <br/>`@member` {import('vue').Ref&lt;string&gt;}

### loading

> 登录请求的加载状态 <br/>`@member` {import('vue').Ref&lt;boolean&gt;}

### showLoginForm

> 控制登录表单的显示状态 <br/>`@member` {import('vue').Ref&lt;boolean&gt;}

### login

> 执行登录操作的方法 <br/>`@function` true<br/>`@async` true<br/>`@returns` undefined

### goToRegister

> 跳转到注册页面的方法 <br/>`@function` true

---

```vue live
<Login />
```
