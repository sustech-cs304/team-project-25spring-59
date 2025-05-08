<template>
  <div class="wrap-container ra-container">
    <div class="ra-content">
      <div class="ra-title">卡路消耗曲线</div>
      <div class="ra-body">
        <div class="wrap-container">
          <div class="chartsdom" id="chart-rollArc"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts' // 在组件中导入 echarts

export default {
  name: 'roll-arcline',
  data() {
  // 生成从3月1日到3月30日的日期
  const startDate = new Date('2025-03-01');  // 设定3月1日为起始日期
  const endDate = new Date('2025-03-30');    // 设定3月30日为结束日期
  const xData = [];  // 存储日期
  const yData = [];  // 存储卡路里消耗值

  // 循环生成日期和卡路里数据
  let currentDate = startDate;
  while (currentDate <= endDate) {
    xData.push(`${currentDate.getMonth() + 1}月${currentDate.getDate()}日`);  // 将日期格式化为 "3月1日"

    // 随机生成卡路里消耗值，假设值在200到600之间
    yData.push(Math.floor(Math.random() * (600 - 200 + 1)) + 200);

    // 日期递增
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return {
    option: null,
    xIndex: 0,
    timer: null,
    xData: xData,  // 日期数据
    yData: yData   // 随机卡路里消耗值
  };
}
,

  mounted() {
    this.getEchart()
  },

  methods: {
    getEchart() {
      // 获取图标渲染体
      const chartRollArc = document.getElementById('chart-rollArc')
      // 初始化图表
      let myChart = echarts.init(chartRollArc)
      this.option = {
        tooltip: {
          trigger: 'axis',
          showContent: true,
          axiosPointer: {
            type: 'shadow',
            shadowStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 1, color: '#5d83ff' },
                { offset: 0, color: 'rgba(255,255,255,0)' }
              ])
            }
          },
          // 重新构造图标信息显示（不写会有默认的格式）
          formatter: (params) => {
            params = params[0]
            if (params.seriesIndex === 0) {
              this.xIndex = parseInt(params.name) - 1
            }
            return (
              params.name + '</br>' + params.seriesName + '：' + params.value + ' 大卡'
            )
          }
        },

        color: ['#5d83ff'],
        grid: {
          top: 30,
          left: 30,
          right: 20,
          bottom: 20,
          containerLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.xData,
          boundaryGap: false,
          axisTick: {
            show: false
          },
          axisLabel: {
            formatter: '{value} '
          },
          axisLine: {
            lineStyle: {
              color: '#999'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            show: false,
            lineStyle: {
              color: '#999'
            }
          }
        },
        series: [
          {
            name: '卡路里',
            type: 'line',
            data: this.yData,
            symbolSize: 10,
            itemStyle: {
              opacity: 0
            },
            emphasis: {
              label: {
                show: true,
                color: '#fff',
                fontSize: 20
              },
              itemStyle: {
                color: '#5d83ff',
                borderColor: '#fff',
                borderWidth: 2,
                opacity: 1
              }
            },
            areaStyle: {
              normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#5d83ff' },
                  { offset: 1, color: 'rgba(0, 0, 0, 0)' }
                ])
              }
            },
            smooth: true
          }
        ]
      }

      // 绘制图表
      myChart.setOption(this.option, true)

      // 监听窗口变化
      window.addEventListener('resize', () => {
        myChart.resize()
      })

      // 开启自动显示信息
      this.startChartAutoShowTip(myChart)

      // 鼠标进入停止自动显示信息
      chartRollArc.onmouseover = () => {
        this.stopChartAutoShowTip()
      }
      // 退出 chartRollArc 继续自动显示信息
      chartRollArc.onmouseout = () => {
        this.startChartAutoShowTip(myChart)
      }
    },

    // 自动显示图标信息函数
    startChartAutoShowTip(myChart) {
      this.stopChartAutoShowTip()

      this.timer = setInterval(() => {
        // 显示图标信息
        myChart.dispatchAction({
          type: 'showTip',
          seriesIndex: 0,
          dataIndex: this.xIndex
        })

        this.xIndex++
        if (this.xIndex > this.yData.length) {
          this.xIndex = 0
        }
      }, 1000)
    },

    // 停止自动显示图标信息函数
    stopChartAutoShowTip() {
      if (this.timer != null) {
        clearInterval(this.timer)
        this.timer = null
      }
    }
  },

  beforeDestroy() {
    // 销毁自动显示信息
    this.stopChartAutoShowTip()
  }
}
</script>

<style lang="scss" scoped>
/* 标题居中 */
.ra-title {
  text-align: center;
  color: white;
}

/* 内容宽高 */
.wrap-container {
  width: 895px;
  height: 400px;

  .chartsdom {
    width: 100%;
    height: 90%;
  }
}
</style>
