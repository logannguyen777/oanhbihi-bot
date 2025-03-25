<template>
  <div class="max-w-5xl mx-auto py-10 px-4 space-y-10">
    <h2 class="text-3xl font-bold text-orange-500 flex items-center gap-2">
      ⚙️ Cấu hình hệ thống
    </h2>

    <SectionCard title="🔑 Cấu hình OpenAI Key">
      <input v-model="config.openai_key" placeholder="OpenAI API Key" class="input input-bordered w-full" />
    </SectionCard>

    <SectionCard title="📩 Cấu hình Facebook Messenger">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input v-model="config.fb_page_token" placeholder="Page Token" class="input input-bordered w-full" />
        <input v-model="config.fb_verify_token" placeholder="Verify Token" class="input input-bordered w-full" />
      </div>
    </SectionCard>

    <SectionCard title="💬 Cấu hình Zalo API">
      <input v-model="config.zalo_verify_token" placeholder="Zalo Verify Token" class="input input-bordered w-full" />
    </SectionCard>

    <SectionCard title="🌐 Cấu hình Crawl dữ liệu">
      <textarea v-model="config.crawl_urls" placeholder="Danh sách URL (mỗi dòng 1 URL)" class="textarea textarea-bordered w-full" rows="4"></textarea>
      <input v-model="config.crawl_schedule" placeholder="Số giờ lập lịch (vd: 24)" class="input input-bordered w-full mt-2" />
    </SectionCard>

    <SaveButton @click="saveAllConfigs" :loading="loading" />

    <div class="space-y-6">
      <h2 class="text-xl font-bold text-orange-500">🧾 Log hệ thống (Realtime)</h2>
      <LogConsole :logs="logs" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getAllConfigs, setConfigByKey } from '@/router/api'
import SectionCard from '@/components/SectionCard.vue'
import SaveButton from '@/components/SaveButton.vue'
import LogConsole from '@/components/LogConsole.vue'

const config = ref({
  openai_key: '',
  fb_page_token: '',
  fb_verify_token: '',
  zalo_verify_token: '',
  crawl_urls: '',
  crawl_schedule: ''
})

const logs = ref([])
const loading = ref(false)
let socket = null

const toast = (msg, type) => window.$toast?.showToast?.(msg, type)

const fetchConfigs = async () => {
  try {
    const res = await getAllConfigs()
    res.data.forEach(item => {
      config.value[item.key] = item.value
    })
  } catch {
    toast('❌ Lỗi tải cấu hình hệ thống!', 'error')
  }
}

const saveAllConfigs = async () => {
  loading.value = true
  try {
    for (const key in config.value) {
      await setConfigByKey(key, config.value[key])
    }
    toast('✅ Đã lưu cấu hình hệ thống!', 'success')
  } catch {
    toast('❌ Lỗi khi lưu cấu hình!', 'error')
  } finally {
    loading.value = false
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
  fetchConfigs()
  connectLogsSocket()
})
onUnmounted(() => socket?.close())
</script>