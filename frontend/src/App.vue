<template>
  <el-container style="height: 100vh; justify-content:center; align-items:center;">
    <el-card style="max-width: 400px; margin: auto;">
      <h2 style="text-align:center;">Shadowverse战绩记录</h2>
      <el-form :model="form" label-width="100px">
        <el-form-item label="己方职业">
          <el-select v-model="form.my_class" placeholder="请选择"> 
            <el-option label="妖" value=1></el-option>
            <el-option label="皇" value=2></el-option>
            <el-option label="法" value=3></el-option>
            <el-option label="龙" value=4></el-option>
            <el-option label="梦" value=5></el-option>
            <el-option label="教" value=6></el-option>
            <el-option label="鱼" value=7></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="己方卡组">
          <el-select v-model="form.my_deck" placeholder="如 Ramp">
            <el-option label="快攻" value=1></el-option>
            <el-option label="中速" value=2></el-option>
            <el-option label="控制" value=3></el-option>
            <el-option label="OTK" value=4></el-option>
            <el-option label="其他" value=5></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="敌方职业">
          <el-select v-model="form.enemy_class" placeholder="请选择"> 
            <el-option label="妖" value=1></el-option>
            <el-option label="皇" value=2></el-option>
            <el-option label="法" value=3></el-option>
            <el-option label="龙" value=4></el-option>
            <el-option label="梦" value=5></el-option>
            <el-option label="教" value=6></el-option>
            <el-option label="鱼" value=7></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="敌方卡组">
          <el-select v-model="form.enemy_deck" placeholder="如 Ramp">
            <el-option label="快攻" value=1></el-option>
            <el-option label="中速" value=2></el-option>
            <el-option label="控制" value=3></el-option>
            <el-option label="OTK" value=4></el-option>
            <el-option label="其他" value=5></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="先后手">
          <el-select v-model="form.first_or_second" placeholder="请选择">
            <el-option label="先手" value=true></el-option>
            <el-option label="后手" value=false></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="胜负结果">
          <el-select v-model="form.is_win" placeholder="请选择">
            <el-option label="胜" value=true></el-option>
            <el-option label="负" value=false></el-option>
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
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import 'element-plus/dist/index.css'

const form = ref({
  my_class: '',
  my_deck: '',
  enemy_class: '',
  enemy_deck: '',
  is_first: '',
  is_win: ''
})

const msg = ref('')

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
    }
  } catch (err) {
    msg.value = err.response?.data?.error || '提交失败'
  }
}
</script>