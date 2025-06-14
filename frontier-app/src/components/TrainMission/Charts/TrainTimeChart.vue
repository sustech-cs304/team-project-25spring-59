<template>
  <div class="wrap-container ra-container">
    <div class="ra-content">
      <div class="ra-title">运动时间曲线</div>
      <div class="ra-body">
        <div class="wrap-container">
          <div class="chartsdom" id="chart-rollArc"></div>
        </div>

        <!-- 月份选择器 -->
        <div class="month-picker">
          <el-date-picker
            v-model="selectedMonth"
            type="month"
            format="YYYY-MM"
            placeholder="选择月份"
            @change="handleMonthChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import dayjs from 'dayjs'
import {API_BASE_URL} from "../../../configs/network_config.js";

export default {
  name: 'roll-arcline',
  data() {
    const now = dayjs()
    return {
      option: null,
      xIndex: 0,
      timer: null,
      xData: [],
      yDataMap: {
        duration: [],
        calories: [],
        avg_hr: [],
        max_hr: []
      },
      selectedMonth: now.format('YYYY-MM')
    }
  },

  mounted() {
    this.generateChartDataForMonth(this.selectedMonth)
    this.getEchart()
  },

  methods: {
    async generateChartDataForMonth(monthStr) {
      const startDate = dayjs(`${monthStr}-01`)
      const endDate = startDate.endOf('month')
      const startStr = startDate.format('YYYY-MM-DD')
      const endStr = endDate.format('YYYY-MM-DD')

      const userId = localStorage.getItem('user_id')
      if (!userId) return

      try {
        const response = await fetch(`${API_BASE_URL}/stats/weekly-trend?start_date=${startStr}&end_date=${endStr}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: parseInt(userId) })
        })
        const data = await response.json()

        this.xData = []
        this.yDataMap = {
          duration: [],
          calories: [],
          avg_hr: [],
          max_hr: []
        }

        // 遍历日期范围
        for (let i = 0; i < endDate.date(); i++) {
          const current = startDate.add(i, 'day')
          const key = current.format('YYYY-MM-DD')
          this.xData.push(current.format('M月D日'))

          const entry = data[key] || {}

          this.yDataMap.duration.push(entry.duration_minutes || 0)
          this.yDataMap.calories.push(entry.calories || 0)
          this.yDataMap.avg_hr.push(entry.avg_heart_rate || 0)
          this.yDataMap.max_hr.push(entry.max_heart_rate || 0)
        }

        this.getEchart()
      } catch (err) {
        console.error('获取趋势数据失败:', err)
      }
    },


    handleMonthChange(val) {
      const formatted = dayjs(val).format('YYYY-MM')
      this.selectedMonth = formatted
      this.generateChartDataForMonth(formatted)
      this.getEchart()
    },

    getEchart() {
      const chartRollArc = document.getElementById('chart-rollArc')
      if (!chartRollArc) return
      let myChart = echarts.init(chartRollArc)

      this.option = {
        tooltip: {
          trigger: 'axis',
          showContent: true,
          formatter: (params) => {
            if (!params || !params.length) return ''
            this.xIndex = params[0].dataIndex

            let tooltipContent = params[0].name + '<br/>'
            params.forEach(item => {
              tooltipContent += `${item.marker}${item.seriesName}：${item.value}<br/>`
            })
            return tooltipContent
          }
        },
        legend: {
          top: 'top',
          data: ['运动时长（分钟）', '消耗卡路里（kcal）', '平均心率（bpm）', '最大心率（bpm）']
        },

        color: ['#5d83ff'],
        grid: {
          top: 30,
          left: 30,
          right: 20,
          bottom: 20,
          containLabel: true
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
            name: '运动时长（分钟）',
            type: 'line',
            data: this.yDataMap.duration,
            symbolSize: 10,
            itemStyle: { opacity: 0 },
            emphasis: {
              label: { show: true, color: '#fff', fontSize: 20 },
              itemStyle: {
                color: '#5d83ff',
                borderColor: '#fff',
                borderWidth: 2,
                opacity: 1
              }
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#5d83ff' },
                { offset: 1, color: 'rgba(0, 0, 0, 0)' }
              ])
            },
            smooth: true
          },
          {
            name: '消耗卡路里（kcal）',
            type: 'line',
            data: this.yDataMap.calories,
            symbolSize: 10,
            itemStyle: { opacity: 0 },
            emphasis: {
              label: { show: true, color: '#fff', fontSize: 20 },
              itemStyle: {
                color: '#4caf50',
                borderColor: '#fff',
                borderWidth: 2,
                opacity: 1
              }
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#4caf50' },
                { offset: 1, color: 'rgba(0, 0, 0, 0)' }
              ])
            },
            smooth: true
          },
          {
            name: '平均心率（bpm）',
            type: 'line',
            data: this.yDataMap.avg_hr,
            symbolSize: 10,
            itemStyle: { opacity: 0 },
            emphasis: {
              label: { show: true, color: '#fff', fontSize: 20 },
              itemStyle: {
                color: '#ff9800',
                borderColor: '#fff',
                borderWidth: 2,
                opacity: 1
              }
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#ff9800' },
                { offset: 1, color: 'rgba(0, 0, 0, 0)' }
              ])
            },
            smooth: true
          },
          {
            name: '最大心率（bpm）',
            type: 'line',
            data: this.yDataMap.max_hr,
            symbolSize: 10,
            itemStyle: { opacity: 0 },
            emphasis: {
              label: { show: true, color: '#fff', fontSize: 20 },
              itemStyle: {
                color: '#f44336',
                borderColor: '#fff',
                borderWidth: 2,
                opacity: 1
              }
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#f44336' },
                { offset: 1, color: 'rgba(0, 0, 0, 0)' }
              ])
            },
            smooth: true
          }
        ]

      }

      myChart.setOption(this.option, true)

      window.addEventListener('resize', () => {
        myChart.resize()
      })

      this.startChartAutoShowTip(myChart)

      chartRollArc.onmouseover = () => {
        this.stopChartAutoShowTip()
      }
      chartRollArc.onmouseout = () => {
        this.startChartAutoShowTip(myChart)
      }
    },

    startChartAutoShowTip(myChart) {
      this.stopChartAutoShowTip()

      this.timer = setInterval(() => {
        myChart.dispatchAction({
          type: 'showTip',
          seriesIndex: 0,
          dataIndex: this.xIndex
        })

        this.xIndex++
        if (this.xIndex >= this.yData.length) {
          this.xIndex = 0
        }
      }, 1000)
    },

    stopChartAutoShowTip() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    }
  },

  beforeDestroy() {
    this.stopChartAutoShowTip()
  }
}
</script>

<style lang="scss" scoped>
.ra-title {
  text-align: center;
  color: white;
}

.wrap-container {
  width: 895px;
  height: 400px;

  .chartsdom {
    width: 100%;
    height: 90%;
  }
}

.month-picker {
  margin-top: 16px;
  text-align: center;
}
</style>
