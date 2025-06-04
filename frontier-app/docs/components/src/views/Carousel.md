# Carousel

## Expose

### isPlaying

> 当前转场动画播放状态 <br/>`@member` {boolean}<br/>`@description` 用于指示转场动画是否正在播放中<br/>`@example` // 在父组件中监测状态<br/>watch(() =&gt; templateRef.value.isPlaying, (val) =&gt; {<br/> console.log('转场状态变化:', val);<br/>});

### showAbout

> 关于弹窗的显示控制状态 <br/>`@member` {boolean}<br/>`@description` 控制"关于我们"弹窗的显示/隐藏状态<br/>`@example` // 在父组件中打开弹窗<br/>templateRef.value.showAbout = true;

### infoItems

> 右上角资源信息配置数组 <br/>`@member` {Array&lt;{image: string, text: string}&gt;}<br/>`@description` 包含 AP 点数、金币、钻石等资源信息的配置数组<br/>`@example` // 在父组件中更新数据<br/>templateRef.value.infoItems = [<br/> { image: "img/ap.png", text: "300/300" },<br/> ...其他数据<br/>];

### studentL2D

> Spine 动画实例数据引用 <br/>`@member` {Object\|null}<br/>`@description` 包含 Live2D 动画的 Spine 实例数据，可用于高级动画控制<br/>`@example` // 在父组件中访问动画数据<br/>console.log('动画数据:', templateRef.value.studentL2D);

### playTransition

> 触发页面转场效果的方法 <br/>`@function` true<br/>`@description` 播放转场动画并在动画结束后自动跳转到仪表盘页面<br/>`@example` // 在父组件中触发转场<br/>templateRef.value.playTransition();

### transitionVideo

> 视频元素 DOM 引用 <br/>`@member` {HTMLVideoElement\|null}<br/>`@description` 转场动画视频元素的直接引用，可用于自定义播放控制<br/>`@warning` 谨慎操作 DOM 元素<br/>`@example` // 在父组件中访问视频元素<br/>templateRef.value.transitionVideo?.pause();

---

```vue live
<Carousel />
```
