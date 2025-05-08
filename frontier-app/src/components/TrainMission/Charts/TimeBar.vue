<template>
  <div class="wrap-container sn-container">
    <div class="sn-content">
      <div class="sn-title">运动时长图</div>
      <div class="sn-body">
        <div class="wrap-container">
          <div class="chartsdom" id="chart-dynamic-bar"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'  // 导入echarts

export default {
  name: 'dynamic-bar',
  data() {
    return {
      option: null,
      dataMap: {}
    }
  },

  mounted() {
    this.getEchart();
  },

  methods: {
    // 处理数据格式
    dataFormatter(obj) {
      let pList = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
      let temp;
      for (let x = 0; x < 3; x++) {
        let max = 0;
        let sum = 0;
        temp = obj[x];
        for (let i = 0, l = temp.length; i < l; i++) {
          max = Math.max(max, temp[i]);
          sum += temp[i];
          obj[x][i] = {
            name: pList[i],
            value: temp[i]
          };
        }
        obj[x + 'max'] = Math.floor(max / 100) * 100;
        obj[x + 'sum'] = sum;
      }
      return obj;
    },

    getEchart() {
      const chartDom = document.getElementById('chart-dynamic-bar'); // 获取 DOM 元素
      const myChart = echarts.init(chartDom); // 使用 echarts 初始化图表

      let itemStyle = {
        barBorderRadius: [15, 0],
        color: '#0084ff'
      };

      // 模拟数据，假设为运动时长（单位：分钟）
      this.dataMap.dataType = this.dataFormatter({
        2: [120, 180, 210, 150, 220, 270, 300, 200, 250, 280, 350, 300], // January to December data
        1: [100, 130, 160, 140, 180, 240, 270, 230, 220, 200, 250, 290],
        0: [80, 110, 150, 130, 190, 220, 240, 220, 210, 250, 270, 280],
      });

      console.log("this.dataMap.dataType", this.dataMap.dataType)

      // 设置图表选项
      this.option = {
        baseOption: {
          timeline: {
            axisType: 'category',
            autoPlay: true,
            playInterval: 1000,
            data: ['游泳', '健身', '跑步'],
            left: 80,
            right: 80,
            bottom: 30,
            lineStyle: {
              color: '#179bf1'
            },
            label: {
              color: '#fff'
            },
            checkpointStyle: {
              color: '#01d8ff',
              symbolSize: 10,
              borderColor: 'rgba(1, 216, 255, 0.5)',
              borderWidth: 5,
            },
            controlStyle: {
              show: false,
            },
            itemStyle: {
              borderColor: '#004b85',
              borderWidth: 1,
              shadowColor: 'rgba(1, 216, 225, 0.5)',
              shadowBlur: 5
            },
            emphasis: {
              label: {
                color: '#01d8ff',
                show: false
              },
              checkpointStyle: {
                color: '#01d8ff',
                borderColor: 'rgba(1, 216, 255, 0.5)',
                borderWidth: 5,
              },
              itemStyle: {
                color: '#01d8ff',
                borderColor: 'rgba(1, 216, 225, 0.5)',
                borderWidth: 5
              }
            }
          },
          calculable: true,
          grid: {
            top: '10%',
            bottom: '35%'
          },
          xAxis: [{
            type: 'category',
            axisLabel: {
              interval: 0
            },
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: '#2867a8',
              }
            },
          }],
          yAxis: [{
            type: 'value',
            name: '运动时长（分钟）',
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: '#2867a8'
              }
            }
          }],
          series: [{
            name: '一类',
            type: 'bar',
            barWidth: 15,
            legendHoverLink: true,
            label: {
              show: true,
              position: 'top',
              color: '#fff'
            },
          }]
        },
        options: [{
          series: [{
            data: this.dataMap.dataType['0'],
            itemStyle: itemStyle
          }]
        }, {
          series: [{
            data: this.dataMap.dataType['1'],
            itemStyle: itemStyle
          }]
        }, {
          series: [{
            data: this.dataMap.dataType['2'],
            itemStyle: itemStyle
          }]
        }]
      }

      // 渲染图表
      myChart.setOption(this.option, true);

      // 监听窗口大小变化
      window.addEventListener('resize', () => {
        myChart.resize();
      });
    }
  }
}
</script>

<style lang="scss" scoped>
  .sn-title {
    text-align: center;
    color: white;
  }
  .sn-container {
    border: 5px solid aqua;
    border-radius: 20px;
  }
  .wrap-container {
    width: 586px;
    height: 400px;
    .chartsdom {
      width: 100%;
      height: 100%;
    }
  }
</style>
