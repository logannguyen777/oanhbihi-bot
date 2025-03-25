<template>
  <div class="max-w-5xl mx-auto py-10 px-4 space-y-10">
    <h2 class="text-3xl font-bold text-orange-500 flex items-center gap-2">
      ⚙️ Cấu hình hệ thống
    </h2>

    <!-- 🔑 OPENAI KEY -->
    <SectionCard title="🔑 Cấu hình OpenAI Key">
      <input v-model="config.openai_key" placeholder="OpenAI API Key" class="input input-bordered w-full" />
    </SectionCard>

    <!-- 🧠 OPENAI MODEL -->
    <SectionCard title="🧠 Mô hình phản hồi (OpenAI)">
      <select v-model="config.openai_model" class="select select-bordered w-full">
        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
        <option value="gpt-4">GPT-4</option>
        <option value="gpt-4-1106-preview">GPT-4 Turbo (Preview)</option>
      </select>
    </SectionCard>

  <!-- 🤖 PERSONA -->
  <SectionCard title="🤖 Tính cách Bot (Persona)">
    <textarea
      v-model="config.persona"
      placeholder="(Prompt ví dụ): Bot là một trợ lý ảo, thân thiện, hài hước, giới tính nữ, 18 tuổi, tên là Oanh.. là nhân viên của Viện công nghệ tài chính, hỗ trợ giải dáp mọi câu hỏi của sinh viên một cách lịch sự, hài hước, hóm hỉnh và tinh tế..."
      class="textarea textarea-bordered w-full"
      rows="3"
    ></textarea>
  </SectionCard>

    <!-- 📩 FACEBOOK MESSENGER -->
    <SectionCard title="📩 Cấu hình Facebook Messenger">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input v-model="config.fb_page_token" placeholder="Page Token" class="input input-bordered w-full" />
        <input v-model="config.fb_verify_token" placeholder="Verify Token" class="input input-bordered w-full" />
      </div>
    </SectionCard>

    <!-- 💬 ZALO -->
    <SectionCard title="💬 Cấu hình Zalo API">
      <input v-model="config.zalo_verify_token" placeholder="Zalo Verify Token" class="input input-bordered w-full" />
    </SectionCard>

    <!-- 🌐 CRAWL -->
    <SectionCard title="🌐 Cấu hình Crawl dữ liệu">
      <textarea v-model="config.crawl_urls" placeholder="Danh sách URL (mỗi dòng 1 URL)" class="textarea textarea-bordered w-full" rows="4"></textarea>
      <input v-model="config.crawl_schedule" placeholder="Số giờ lập lịch (vd: 24)" class="input input-bordered w-full mt-2" />
    </SectionCard>

    <!-- 💾 SAVE -->
    <SaveButton @click="saveAllConfigs" :loading="loading" />

    <!-- 🌐 Huấn luyện ngay từ URL -->
    <SectionCard title="🚀 Huấn luyện ngay từ URL (demo)">
      <button class="btn btn-warning w-full" @click="crawlAndTrainNow">Crawl & Huấn luyện ngay</button>
    </SectionCard>

    <!-- 🧾 LOG -->
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
  openai_model: '',
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
    config.value = { ...config.value, ...res.data }  // ✅ Merge luôn object
  } catch {
    toast('❌ Lỗi tải cấu hình hệ thống!', 'error')
  }
}

import { crawlInstantUrl } from '@/router/api'

const crawlAndTrainNow = async () => {
  if (!config.value.crawl_urls) return window.$toast.showToast('❌ Chưa nhập URL!', 'error')
  try {
    await crawlInstantUrl(config.value.crawl_urls.split('\n')[0])  // chỉ crawl URL đầu tiên
    window.$toast.showToast('✅ Đã crawl & huấn luyện!', 'success')
  } catch {
    window.$toast.showToast('❌ Lỗi crawl & huấn luyện', 'error')
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
