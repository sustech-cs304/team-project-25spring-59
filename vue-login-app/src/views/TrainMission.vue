<template>
  <div class="training-container">
    <h2>🏋️ 训练任务管理</h2>

    <!-- 任务创建 -->
    <el-card class="task-form">
      <h3>➕ 添加新任务</h3>
      <el-form label-width="120px">
        <el-form-item label="任务名称">
          <el-input v-model="newTask.name" placeholder="输入训练任务名称" />
        </el-form-item>
        <el-form-item label="任务类型">
          <el-select v-model="newTask.type" placeholder="选择训练类型">
            <el-option label="有氧运动" value="cardio"></el-option>
            <el-option label="力量训练" value="strength"></el-option>
            <el-option label="瑜伽" value="yoga"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="训练日期">
          <el-date-picker v-model="newTask.date" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="开始时间">
          <el-time-picker v-model="newTask.startTime" placeholder="选择开始时间" />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-time-picker v-model="newTask.endTime" placeholder="选择结束时间" @change="calculateDuration" />
        </el-form-item>
        <el-form-item label="目标 (分钟)">
          <el-input-number v-model="newTask.goal" :min="10" :max="300" disabled />
        </el-form-item>
        <el-button type="primary" @click="addTask">添加任务</el-button>
      </el-form>
    </el-card>

    <!-- 任务列表 -->
    <el-card class="task-list">
      <h3>📅 训练任务列表</h3>
      <el-table :data="tasks" style="width: 100%" :row-class-name="tableRowClass">
        <el-table-column prop="name" label="任务名称" width="150"></el-table-column>
        <el-table-column prop="type" label="类型" width="120"></el-table-column>
        <el-table-column prop="date" label="日期" width="120"></el-table-column>
        <el-table-column prop="startTime" label="开始时间" width="120"></el-table-column>
        <el-table-column prop="endTime" label="结束时间" width="120"></el-table-column>
        <el-table-column prop="goal" label="时长 (分钟)" width="120"></el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-checkbox v-model="row.completed" @change="toggleCompletion(row)">
              {{ row.completed ? "已完成" : "未完成" }}
            </el-checkbox>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="danger" @click="deleteTask(row)">🗑️ 删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElNotification } from 'element-plus';

const newTask = ref({
  name: '',
  type: '',
  date: '',
  startTime: '',
  endTime: '',
  goal: 0,
});

const tasks = ref([]);
const activeReminders = ref({}); // 存储激活的提醒，防止重复提醒

//计算持续时间
const calculateDuration = () => {
  if (newTask.value.startTime && newTask.value.endTime) {
    const start = new Date(newTask.value.startTime).getTime();
    const end = new Date(newTask.value.endTime).getTime();

    if (end > start) {
      newTask.value.goal = Math.floor((end - start) / 60000); // 计算分钟数
    } else {
      ElMessage.error("结束时间必须大于开始时间");
      newTask.value.endTime = null; // 清空错误时间
    }
  }
};


const addTask = () => {
  if (!newTask.value.name || !newTask.value.type || !newTask.value.date || !newTask.value.startTime || !newTask.value.endTime) {
    ElMessage.error('请填写完整的任务信息');
    return;
  }

  tasks.value.push({
    id: Date.now(),
    name: newTask.value.name,
    type: newTask.value.type,
    date: newTask.value.date,
    startTime: new Date(newTask.value.startTime), // 确保存储的是 Date
    endTime: new Date(newTask.value.endTime),     // 确保存储的是 Date
    goal: Math.floor((new Date(newTask.value.endTime) - new Date(newTask.value.startTime)) / 60000),
    completed: false
  });

  ElMessage.success('任务添加成功');
  newTask.value = { name: '', type: '', date: '', startTime: '', endTime: '', goal: 0 };
};


const deleteTask = (task) => {
  tasks.value = tasks.value.filter(t => t.id !== task.id);
  ElMessage.success(`任务 "${task.name}" 已删除`);
};



const toggleCompletion = (task) => {
  const index = tasks.value.findIndex(t => t.id === task.id);
  if (index !== -1) {
    // 先切换状态
    const updatedTask = { ...tasks.value[index], completed: !tasks.value[index].completed };

    // 让 Vue 重新渲染
    tasks.value[index] = updatedTask;

    // 使用最新的状态进行提示
    ElMessage.success(`任务 "${updatedTask.name}" 状态已更新为 ${updatedTask.completed ? "已完成" : "未完成"}`);

    // 任务完成后取消提醒
    if (updatedTask.completed) {
      delete activeReminders.value[updatedTask.id];
    }
  }
};




//状态栏自动变绿，切换组件
const tableRowClass = ({ row }) => {
  return row.completed ? 'completed-row' : ''; // 如果任务已完成，应用 'completed-row' 样式
};



const checkReminders = () => {
  const now = new Date().getTime();
  console.log(`🕒 当前时间: ${new Date().toLocaleTimeString()}`);

  tasks.value.forEach(task => {
    if (!task.completed) {
      console.log(`📅 任务 "${task.name}" 的 startTime:`, task.startTime);

      // 确保 startTime 是 Date 类型
      let startTime;
      if (task.startTime instanceof Date) {
        startTime = task.startTime;
      } else {
        console.error(`❌ 任务 "${task.name}" 的 startTime 类型错误:`, typeof task.startTime);
        return;
      }

      const reminderTime = startTime.getTime() - 5 * 60 * 1000; // 开始前 5 分钟

      console.log(`⏳ 预计提醒时间: ${new Date(reminderTime)}`);

      if (now >= reminderTime && now < startTime.getTime()) {
        console.log(`🚀 触发提醒: ${task.name}`);

        if (!activeReminders.value[task.id] || now - activeReminders.value[task.id] > 10 * 1000) {
          activeReminders.value[task.id] = now;

          ElNotification({
            title: "⏳ 训练提醒",
            message: `⚠️ 训练 "${task.name}" 即将开始！`,
            type: "warning",
            duration: 0, // 不自动关闭
            onClose: () => {
              delete activeReminders.value[task.id]; // 允许下一次提醒
            }
          });
        }
      } else {
        if (now >= startTime.getTime()) {
          delete activeReminders.value[task.id];
        }
      }
    }
  });
};



// 每秒检查一次任务提醒
onMounted(() => {
  setInterval(checkReminders, 1000);
});





</script>



<style>
/* 让已完成任务的行背景变绿 */
.completed-row {
  background-color: #d4edda !important; /* 绿色背景 */
  color: #155724 !important; /* 深绿色文本 */
}

.training-container {
  max-width: 900px;
  margin: 20px auto;
  text-align: center;
}

.task-form {
  margin-bottom: 20px;
  padding: 20px;
}

.task-list {
  padding: 20px;
}
</style>
