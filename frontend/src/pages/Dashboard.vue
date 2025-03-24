<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-6">📊 Tổng Quan Hệ Thống</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">🔐 OpenAI API Key</h2>
          <p>{{ openai_status }}</p>
        </div>
      </div>

      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">🧠 Personas</h2>
          <p>{{ stats.personas }} bot persona</p>
        </div>
      </div>

      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">🌐 Crawl URLs</h2>
          <p>{{ stats.crawls }} cấu hình URL</p>
        </div>
      </div>

      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">📄 Dữ liệu web_pages</h2>
          <p>{{ stats.pages }} mẫu, {{ stats.embedding }} đã embedding</p>
        </div>
      </div>

      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">📡 WebSocket</h2>
          <p>Đang {{ socket_status ? '🟢 hoạt động' : '🔴 lỗi' }}</p>
        </div>
      </div>
    </div>
  </div>

  <div class="space-y-6">
    <h2 class="text-xl font-bold text-orange-500">🧾 Log hệ thống (Realtime)</h2>
    <LogConsole :logs="logs" />
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../router/api'
import { io } from 'socket.io-client'
import { ref, onMounted, onUnmounted } from 'vue'
import LogConsole from '@/components/ui/LogConsole.vue'

const stats = ref({
  personas: 0,
  crawls: 0,
  pages: 0,
  embedding: 0
})

const openai_status = ref("Đang kiểm tra...")
const socket_status = ref(false)

const fetchStats = async () => {
  try {
    const [p, c, w, o] = await Promise.all([
      axios.get('/api/persona'),
      axios.get('/api/crawl'),
      axios.get('/api/training/web-pages'),
      axios.get('/api/config?key=openai_key')
    ])
    stats.value.personas = p.data.length
    stats.value.crawls = c.data.length
    stats.value.pages = w.data.length
    stats.value.embedding = w.data.filter(x => x.embedding).length
    openai_status.value = o.data.value ? '✅ Có cấu hình' : '⚠️ Thiếu API Key'
  } catch (e) {
    openai_status.value = '❌ Lỗi kết nối'
  }
}

const checkSocket = () => {
  const socket = io('/ws')
  socket.on('connect', () => {
    socket_status.value = true
    socket.disconnect()
  })
  socket.on('connect_error', () => {
    socket_status.value = false
  })
}

onMounted(() => {
  fetchStats()
  checkSocket()
})


const logs = ref([])
let socket = null

const connectLogsSocket = () => {
  socket = new WebSocket('ws://localhost:8000/ws/logs') // 👈 đổi nếu dùng domain hoặc port khác

  socket.onmessage = (event) => {
    logs.value.push(event.data)
  }

  socket.onopen = () => {
    logs.value.push('[📡] Đã kết nối WebSocket')
  }

  socket.onclose = () => {
    logs.value.push('[❌] Mất kết nối WebSocket')
  }

  socket.onerror = () => {
    logs.value.push('[⚠️] WebSocket lỗi kết nối')
  }
}

onMounted(() => {
  connectLogsSocket()
})

onUnmounted(() => {
  socket?.close()
})



</script>