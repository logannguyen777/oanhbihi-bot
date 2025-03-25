<template>
  <div id="app" class="min-h-screen bg-base-100 text-base-content">
    <RouterView />
    <GlobalLogConsole :logs="logs" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GlobalLogConsole from './components/GlobalLogConsole.vue'

const logs = ref([])

onMounted(() => {
  const socket = new WebSocket('ws://localhost:8000/ws/logs')

  socket.onmessage = (event) => {
    const msg = event.data
    if (msg !== '__chat_update__') {
      logs.value.push(msg)
    } else {
      console.log('📥 Nhận tín hiệu cập nhật chat từ backend')
      // Tùy ý xử lý cập nhật UI khi có chat_update
    }
  }

  socket.onopen = () => {
    console.log('✅ WebSocket kết nối thành công!')
  }

  socket.onerror = (err) => {
    console.error('❌ WebSocket lỗi:', err)
  }

  socket.onclose = () => {
    console.warn('🔌 WebSocket bị đóng!')
  }
})
</script>
