<template>
  <div class="max-w-5xl mx-auto py-10 px-4 space-y-10">
    <h2 class="text-3xl font-bold text-orange-500 flex items-center gap-2">
      ⚙️ Cấu hình hệ thống
    </h2>

    <!-- 1. MESSENGER CONFIG -->
    <SectionCard title="📩 Cấu hình Messenger">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input v-model="messenger.pageToken" placeholder="Page Token" class="input input-bordered w-full" />
        <input v-model="messenger.verifyToken" placeholder="Verify Token" class="input input-bordered w-full" />
      </div>
      <SaveButton @click="saveMessenger" :loading="loading" />
    </SectionCard>

    <!-- 2. PERSONA CONFIG -->
    <SectionCard title="🧍‍♀️ Cấu hình Persona (Bot Oanh Bihi)">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input v-model="persona.name" placeholder="Tên Bot" class="input input-bordered w-full" />
        <input v-model="persona.age" placeholder="Tuổi" class="input input-bordered w-full" />
        <input v-model="persona.gender" placeholder="Giới tính" class="input input-bordered w-full" />
        <input v-model="persona.tone" placeholder="Giọng điệu" class="input input-bordered w-full" />
        <input v-model="persona.style" placeholder="Phong cách" class="input input-bordered w-full" />
        <input v-model="persona.greeting" placeholder="Lời chào" class="input input-bordered w-full" />
      </div>
      <SaveButton @click="savePersona" :loading="loading" />
    </SectionCard>

    <!-- 3. CRAWL CONFIG -->
    <SectionCard title="🌐 Cấu hình Crawl dữ liệu">
      <textarea
        v-model="crawl.urls"
        placeholder="Danh sách URL (mỗi dòng 1 URL)"
        class="textarea textarea-bordered w-full"
        rows="4"
      ></textarea>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
        <input v-model="crawl.fileTypes" placeholder="File Types (vd: pdf,docx)" class="input input-bordered w-full" />
        <input v-model="crawl.schedule" placeholder="Schedule (vd: daily, weekly)" class="input input-bordered w-full" />
      </div>
      <SaveButton @click="saveCrawl" :loading="loading" />
    </SectionCard>

    <!-- 4. DYNAMIC CONFIG -->
    <SectionCard title="🔧 Cấu hình chung từ hệ thống (AppConfig)">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="(value, key) in dynamicConfig" :key="key" class="form-control">
          <label class="label"><span class="label-text capitalize">{{ key.replaceAll('_', ' ') }}</span></label>
          <input v-model="dynamicConfig[key]" class="input input-bordered w-full" />
        </div>
      </div>
      <SaveButton @click="saveDynamicConfig" :loading="loading" />
    </SectionCard>
  </div>

  <div class="space-y-6">
    <h2 class="text-xl font-bold text-orange-500">🧾 Log hệ thống (Realtime)</h2>
    <LogConsole :logs="logs" />
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/router/api'
import SectionCard from '@/components/ui/SectionCard.vue'
import SaveButton from '@/components/ui/SaveButton.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import LogConsole from '@/components/ui/LogConsole.vue'


const loading = ref(false)

const messenger = ref({ pageToken: '', verifyToken: '' })
const persona = ref({ name: '', age: '', gender: '', tone: '', greeting: '', style: '' })
const crawl = ref({ urls: '', fileTypes: '', schedule: '' })
const dynamicConfig = ref({})

onMounted(async () => {
  try {
    const res = await api.get('/api/config')
    dynamicConfig.value = res.data
  } catch (e) {
    toast('❌ Lỗi tải cấu hình động', 'error')
  }
})

const saveMessenger = async () => {
  await saveSection('/api/config/messenger', messenger.value, 'Messenger')
}

const savePersona = async () => {
  await saveSection('/api/config/persona', persona.value, 'Persona')
}

const saveCrawl = async () => {
  const payload = {
    urls: crawl.value.urls.split('\n').filter(Boolean),
    fileTypes: crawl.value.fileTypes.split(',').map(x => x.trim()),
    schedule: crawl.value.schedule,
  }
  await saveSection('/api/config/crawl', payload, 'Crawl')
}

const saveDynamicConfig = async () => {
  for (const key in dynamicConfig.value) {
    await api.post('/api/config', null, { params: { key, value: dynamicConfig.value[key] } })
  }
  toast('✅ Đã lưu cấu hình hệ thống!', 'success')
}

const saveSection = async (url, data, label) => {
  loading.value = true
  try {
    await api.post(url, data)
    toast(`✅ Lưu ${label} thành công!`, 'success')
  } catch {
    toast(`❌ Lỗi khi lưu ${label}!`, 'error')
  } finally {
    loading.value = false
  }
}

const toast = (msg, type) => {
  window.$toast?.showToast?.(msg, type)
}


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
