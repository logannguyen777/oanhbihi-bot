<template>
  <div id="app" class="min-h-screen bg-base-100 text-base-content">
    <RouterView />
    <GlobalLogConsole :logs="logs" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GlobalLogConsole from './components/GlobalLogConsole.vue'
import { isLoggedIn } from '@/router/auth'
import { useRouter } from 'vue-router'


const router = useRouter()
const logs = ref([])

onMounted(() => {

  if (!isLoggedIn() && router.currentRoute.value.name !== 'Login') {
    router.push({ name: 'Login' })
  }

  const socket = new WebSocket(
    `${location.protocol === 'https:' ? 'wss' : 'ws'}://backend.fta.thefirst.ai/ws/logs`
  )
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
