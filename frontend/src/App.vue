<template>
  <el-row style="height: 100vh;">
    <!-- 左侧表单 -->
    <el-col :span="12" style="display: flex; justify-content: center; align-items: center;">
      <el-card style="max-width: 400px; width: 100%; margin: auto;">
        <h2 style="text-align:center;">Shadowverse战绩记录</h2>
        <el-form :model="form" label-width="100px">
         <el-form-item label="用户标识符">
          <el-input v-model="form.user_identifier" placeholder="必须，用户唯一标识"></el-input>
         </el-form-item>
          <el-form-item label="己方职业">
            <el-select v-model="form.my_class" placeholder="请选择">
              <el-option label="妖" :value="1"></el-option>
              <el-option label="皇" :value="2"></el-option>
              <el-option label="法" :value="3"></el-option>
              <el-option label="龙" :value="4"></el-option>
              <el-option label="梦" :value="5"></el-option>
              <el-option label="教" :value="6"></el-option>
              <el-option label="鱼" :value="7"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="己方卡组">
            <el-select v-model="form.my_deck" placeholder="如 Ramp">
              <el-option label="快攻" value="快攻"></el-option>
              <el-option label="中速" value="中速"></el-option>
              <el-option label="控制" value="控制"></el-option>
              <el-option label="OTK" value="OTK"></el-option>
              <el-option label="其他" value="其他"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="敌方职业">
            <el-select v-model="form.enemy_class" placeholder="请选择">
              <el-option label="妖" :value="1"></el-option>
              <el-option label="皇" :value="2"></el-option>
              <el-option label="法" :value="3"></el-option>
              <el-option label="龙" :value="4"></el-option>
              <el-option label="梦" :value="5"></el-option>
              <el-option label="教" :value="6"></el-option>
              <el-option label="鱼" :value="7"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="敌方卡组">
            <el-select v-model="form.enemy_deck" placeholder="如 Ramp">
              <el-option label="快攻" value="快攻"></el-option>
              <el-option label="中速" value="中速"></el-option>
              <el-option label="控制" value="控制"></el-option>
              <el-option label="OTK" value="OTK"></el-option>
              <el-option label="其他" value="其他"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="先后手">
            <el-select v-model="form.is_first" placeholder="请选择">
              <el-option label="先手" :value="true"></el-option>
              <el-option label="后手" :value="false"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="胜负结果">
            <el-select v-model="form.is_win" placeholder="请选择">
              <el-option label="胜" :value="true"></el-option>
              <el-option label="负" :value="false"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交记录</el-button>
          </el-form-item>
        </el-form>
        <el-alert
          v-if="msg"
          :title="msg"
          type="success"
          show-icon
          style="margin-top: 10px;"
          :closable="false"
        />
      </el-card>
    </el-col>
    <!-- 右侧饼图及切换 -->
    <el-col :span="12" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <div style="width: 350px;">
        <el-select v-model="recordCount" style="width: 120px; margin-bottom: 20px;" @change="fetchAllCharts">
          <el-option label="最近20场" :value="20" />
          <el-option label="最近50场" :value="50" />
          <el-option label="最近100场" :value="100" />
        </el-select>
        <v-chart :option="pieOption" autoresize style="height: 350px;" v-if="pieOption" />
        <v-chart :option="lineOption" autoresize style="height: 250px; margin-top: 30px;" v-if="lineOption" />
      </div>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import VChart from "vue-echarts"
import 'element-plus/dist/index.css'

// 必须引入对应ECharts组件
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { use } from 'echarts/core'
import { time } from 'echarts'

use([
  CanvasRenderer,
  PieChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
])

// 职业映射
const classMap = {
  1: "妖",
  2: "皇",
  3: "法",
  4: "龙",
  5: "梦",
  6: "教",
  7: "鱼"
}

const form = ref({
  my_class: '',
  my_deck: '',
  enemy_class: '',
  enemy_deck: '',
  is_first: '',
  is_win: '',
  time_stamp: Math.floor(new Date().getTime() / 1000),
  user_identifier: '' 
})

const msg = ref('')
const recordCount = ref(20)
const pieOption = ref(null)
const lineOption = ref(null)

// 饼图数据
const fetchPieData = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/records?limit=${recordCount.value}`)
    // 统计敌方职业分布
    const counter = {}
    for (const rec of res.data) {
      const c = rec.enemy_class
      counter[c] = (counter[c] || 0) + 1
    }
    const pieData = Object.entries(counter).map(([k, v]) => ({
      name: classMap[k] || k,
      value: v
    }))
    pieOption.value = {
      title: { text: `敌方职业分布（最近${recordCount.value}场）`, left: 'center' },
      tooltip: { trigger: 'item' },
      series: [
        {
          name: '职业',
          type: 'pie',
          radius: '60%',
          data: pieData,
          label: { formatter: '{b}: {d}%' }
        }
      ]
    }
  } catch (e) {
    pieOption.value = null
  }
}

// 折线图数据
const fetchLineData = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/records?limit=${recordCount.value}`)
    const records = res.data
    records.reverse() // 从最早到最新
    let winCount = 0
    let rateData = []
    let xData = []
    records.forEach((rec, idx) => {
      if (rec.is_win) winCount++
      rateData.push(Number(((winCount / (idx + 1)) * 100).toFixed(2)))
      xData.push(idx + 1)
    })
    lineOption.value = {
      title: { text: `最近${recordCount.value}场胜率趋势`, left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: xData,
        name: '对局数'
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        axisLabel: { formatter: '{value}%' }
      },
      series: [
        {
          name: '累计胜率',
          type: 'line',
          data: rateData,
          smooth: true,
          symbol: 'circle'
        }
      ]
    }
  } catch (e) {
    lineOption.value = null
  }
}

const fetchAllCharts = async () => {
  await fetchPieData()
  await fetchLineData()
}

onMounted(fetchAllCharts)

const submitForm = async () => {
  try {
    const response = await axios.post('http://localhost:5000/add_record', form.value)
    msg.value = '提交成功！ID: ' + response.data.id
    form.value = {
      my_class: '',
      my_deck: '',
      enemy_class: '',
      enemy_deck: '',
      is_first: '',
      is_win: '',
      time_stamp: 0,
      user_identifier: ''
    }
    fetchAllCharts()
  } catch (err) {
    msg.value = err.response?.data?.error || '提交失败'
  }
}
</script>

<style scoped>
/* 可自定义样式 */
</style>