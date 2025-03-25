<!-- 📁 src/components/Sidebar.vue -->
<template>
    <ul class="menu p-4 w-60 min-h-full bg-black text-base-content">
      <h2 class="text-xl font-bold mb-4 text-primary">🌸 DNU-FTA Agent</h2>
      <li><router-link to="/dashboard">📊 Dashboard</router-link></li>
      <li><router-link to="/chat">💬 Chat</router-link></li>
      <li><router-link to="/train">🧠 Huấn luyện</router-link></li>
      <li><router-link to="/settings">⚙️ Cấu hình</router-link></li>
      <li><router-link to="/admin-chat">👩‍💼 Admin Chat</router-link></li>
      <li>
        <button @click="handleLogout" class="btn btn-outline btn-error w-full mt-2">
          🚪 Đăng xuất
        </button>
      </li>
    </ul>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  import { logout } from '@/router/auth'
  
  const router = useRouter()
  
  const handleLogout = () => {
    logout(router)
  }
  </script>
  