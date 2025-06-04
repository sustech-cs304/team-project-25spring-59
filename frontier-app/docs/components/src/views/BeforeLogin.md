# BeforeLogin

## Expose

### isLoading

> 是否显示加载动画 <br/>`@member` {boolean}

### progress

> 加载进度百分比 <br/>`@member` {number}

### statusText

> 状态显示文本 <br/>`@member` {string}

### showLoginButton

> 是否显示登录按钮提示 <br/>`@member` {boolean}

### initializeApp

> 初始化应用 <br/>`@method` true<br/>`@async` true

### checkServerStatus

> 检查服务器是否可用 <br/>`@method` true<br/>`@async` true

### preloadAssets

> 预加载资源 <br/>`@method` true<br/>`@async` true<br/>`@returns` undefined

### simulateLoadingStep

> 模拟加载步骤 <br/>`@method` true<br/>`@async` true<br/>`@param` 进度百分比<br/>`@returns` undefined

### goToLogin

> 跳转到登录界面 <br/>`@method` true

---

```vue live
<BeforeLogin />
```
