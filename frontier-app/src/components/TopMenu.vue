<script setup>
/**
 *  顶部导航栏
 */
</script>

<template>
  <el-affix position="top">
    <el-row class="top-menu-row">
      <el-col :span="10" :offset="7">
        <el-menu
            mode="horizontal"
            router
            class="top-menu"
            :ellipsis="false"
        >
          <el-menu-item
              index="1"
              route="/carousel"
              class="home-menu-item"
          >
            <span class="menu-text">回到首页</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </el-affix>
</template>

<style scoped>
.top-menu-row {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.top-menu {
  background: transparent;
  border-bottom: none;
}

.home-menu-item {
  font-size: 16px;
  font-weight: 500;
  color: #2c3e50;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
}

.home-menu-item:hover {
  color: #409eff;
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.menu-text {
  position: relative;
}

.menu-text::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -5px;
  left: 0;
  background-color: #409eff;
  transition: width 0.3s ease;
}

.home-menu-item:hover .menu-text::after {
  width: 100%;
}
</style>