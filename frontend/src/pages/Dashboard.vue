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
          <p>hihi</p>
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

    <div class="mt-8 space-y-6">
      <h2 class="text-xl font-bold text-orange-500">🧾 Log hệ thống (Realtime)</h2>
      <LogConsole :logs="logs" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getCrawls, getWebPages, getAllConfigs } from '@/router/api'
import LogConsole from '@/components/LogConsole.vue'

const stats = ref({
  crawls: 0,
  pages: 0,
  embedding: 0
})

const openai_status = ref("Đang kiểm tra...")
const socket_status = ref(false)
const logs = ref([])
let socket = null

const fetchStats = async () => {
  try {
    const [p, c, w, o] = await Promise.all([
      
      getCrawls(),
      getWebPages(),
      getAllConfigs()
    ])
    stats.value.crawls = c.data.length
    stats.value.pages = w.data.length
    stats.value.embedding = w.data.filter(x => x.embedding).length
    openai_status.value = o.data.openai_key ? '✅ Có cấu hình' : '⚠️ Thiếu API Key'
  } catch (e) {
    openai_status.value = '❌ Lỗi kết nối'
  }
}

const checkSocket = () => {
  const socket = new WebSocket(import.meta.env.VITE_BACKEND_WS || 'ws://localhost:8000/ws/logs')
  socket.onopen = () => {
    socket_status.value = true
    socket.close()
  }
  socket.onerror = () => {
    socket_status.value = false
  }
}

const connectLogsSocket = () => {
  socket = new WebSocket(import.meta.env.VITE_BACKEND_WS || 'ws://localhost:8000/ws/logs')
  socket.onmessage = (event) => logs.value.push(event.data)
  socket.onopen = () => logs.value.push('[📡] Đã kết nối WebSocket')
  socket.onclose = () => logs.value.push('[❌] Mất kết nối WebSocket')
  socket.onerror = () => logs.value.push('[⚠️] WebSocket lỗi kết nối')
}

onMounted(() => {
  fetchStats()
  checkSocket()
  connectLogsSocket()
})

onUnmounted(() => {
  socket?.close()
})
</script>