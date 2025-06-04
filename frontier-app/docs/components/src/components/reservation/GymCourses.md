# GymCourses

## Props

| Prop name | Description | Type      | Values | Default |
| --------- | ----------- | --------- | ------ | ------- |
| gymId     |             | undefined | -      |         |
| gymName   |             | undefined | -      |         |

## Expose

### userId

> 当前用户 ID <br/>`@member` {string}

### props

> 组件属性 <br/>`@member` {Object}<br/>`@property` 健身房名称

### groupByDate

> 按日期分组的课程数据 <br/>`@member` {Object}

### dateList

> 日期列表 <br/>`@member` {Object}

### currentCourses

> 当前显示的课程列表 <br/>`@member` {Object}

### personalCourses

> 用户已预约的课程 ID 列表 <br/>`@member` {Array}

### index

> 当前显示的日期索引 <br/>`@member` {Object}

### range

> 每次显示的日期范围大小 <br/>`@member` {Object}

### isLoading

> 加载状态 <br/>`@member` {Object}

### isReserved

> 检查课程是否已被预约 <br/>`@function` true

### processCourses

> 处理课程数据 <br/>`@function` true

### formatTime

> 格式化时间 <br/>`@function` true

### getPersonalCourses

> 获取用户已预约课程 <br/>`@function` true

### reserveCourse

> 预约课程 <br/>`@function` true

### handleDateClick

> 处理日期点击 <br/>`@function` true

### handlePrevClick

> 处理向前翻页 <br/>`@function` true

### handleNextClick

> 处理向后翻页 <br/>`@function` true

---

```vue live
<GymCourses />
```
