<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import LogConsole from '@/components/LogConsole.vue'
import {
  uploadTrainFiles,
  startTraining,
  getTrainedDocs,
  crawlUrl,
  crawlInstantUrl
} from '@/router/api'

const files = ref([])
const loading = ref(false)
const training = ref(false)
const logs = ref([])
const url = ref('')
const selectedModel = ref('text-embedding-ada-002')
const trainedDocs = ref([])
const logRef = ref(null)

const handleFileChange = (e) => {
  files.value = Array.from(e.target.files)
}

const uploadFiles = async () => {
  if (!files.value.length) return
  loading.value = true
  const formData = new FormData()
  files.value.forEach((file) => formData.append('files', file))

  try {
    await uploadTrainFiles(formData)
    window.$toast?.showToast('✅ Upload thành công!', 'success')
    await fetchTrainedDocs()
    files.value = []
  } catch (err) {
    window.$toast?.showToast('❌ Upload thất bại!', 'error')
  } finally {
    loading.value = false
  }
}

const startTrainingHandler = async () => {
  training.value = true
  try {
    const res = await startTraining()
    logs.value.push(res.data.stdout || '')
    logs.value.push(res.data.stderr || '')
    window.$toast?.showToast('✅ Huấn luyện hoàn tất!', 'success')
    await fetchTrainedDocs()
  } catch (err) {
    window.$toast?.showToast('❌ Huấn luyện thất bại!', 'error')
  } finally {
    training.value = false
  }
}

const fetchTrainedDocs = async () => {
  const res = await getTrainedDocs()
  trainedDocs.value = [...res.data.uploads, ...res.data.web]
}

const crawlAndTrain = async () => {
  if (!url.value || !url.value.trim()) {
    window.$toast?.showToast('⚠️ Vui lòng nhập URL trước khi crawl!', 'warning')
    return
  }

  try {
    await crawlInstantUrl(url.value)
    window.$toast?.showToast('✅ Crawl thành công!', 'success')
    url.value = ''
    await startTrainingHandler()
  } catch (err) {
    console.error("❌ Lỗi khi crawl:", err)
    window.$toast?.showToast('❌ Crawl thất bại!', 'error')
  }
}

// Tự động scroll log xuống cuối
watch(logs, async () => {
  await nextTick()
  const el = logRef.value?.$el || logRef.value
  if (el) el.scrollTop = el.scrollHeight
})

onMounted(() => {
  const ws = new WebSocket(import.meta.env.VITE_BACKEND_WS || `ws://${window.location.host}/ws/logs`)
  ws.onmessage = (event) => {
    logs.value.push(event.data)
  }
  fetchTrainedDocs()
})
</script>

<template>
  <div class="max-w-5xl mx-auto mt-10 space-y-6">
    <h2 class="text-2xl font-bold text-primary">🧠 Huấn luyện DNU-FTA Bot</h2>

    <!-- Upload Files -->
    <div class="bg-black rounded-xl shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">📁 Upload tài liệu</h3>
      <input type="file" multiple @change="handleFileChange" class="file-input file-input-bordered w-full" />
      <ul v-if="files.length" class="text-sm text-white list-disc pl-5">
        <li v-for="(file, i) in files" :key="i">{{ file.name }}</li>
      </ul>
      <button class="btn btn-secondary w-full" :disabled="!files.length || loading" @click="uploadFiles">
        <span v-if="loading" class="loading loading-spinner"></span>
        <span v-else>📤 Upload tài liệu</span>
      </button>
    </div>

    <!-- Crawl URL -->
    <div class="bg-black rounded-xl shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">🌐 Crawl & Train từ URL</h3>
      <input v-model="url" type="text" placeholder="Nhập URL..." class="input input-bordered w-full" />
      <button class="btn btn-accent w-full mt-2" :disabled="!url || training" @click="crawlAndTrain">
        <span v-if="training" class="loading loading-spinner"></span>
        <span v-else>🌐 Crawl và Huấn luyện</span>
      </button>
    </div>

    <!-- Select Model -->
    <div class="bg-black rounded-xl shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">🧠 Chọn mô hình embedding</h3>
      <select v-model="selectedModel" class="select select-bordered w-full">
        <option value="text-embedding-ada-002">OpenAI - Ada</option>
        <option value="all-MiniLM-L6-v2">MiniLM (local)</option>
        <option value="InstructorXL">Instructor XL (local)</option>
      </select>
    </div>

    <!-- Start Training -->
    <div class="bg-black rounded-xl shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">⚙️ Bắt đầu huấn luyện</h3>
      <button
        class="btn btn-primary"
        :disabled="training"
        @click="startTrainingHandler">
        <span v-if="training" class="loading loading-spinner"></span>
        <span v-else>Huấn luyện ngay</span>
      </button>

    </div>

    <!-- Logs -->
    <div class="bg-black rounded-xl shadow p-4 space-y-3 max-h-[300px] overflow-y-auto" ref="logRef">
      <h3 class="text-lg font-semibold">📜 Log quá trình huấn luyện</h3>
      <LogConsole :logs="logs" />
    </div>

    <!-- Trained Documents Table -->
    <div class="bg-black rounded-xl shadow p-4 space-y-3 overflow-auto">
      <h3 class="text-lg font-semibold">📊 Danh sách tài liệu đã huấn luyện</h3>
      <table class="table w-full text-white table-zebra">
        <thead>
          <tr>
            <th>Tên tài liệu</th>
            <th>Nguồn</th>
            <th>Số đoạn</th>
            <th>Thời gian</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in trainedDocs" :key="doc.id">
            <td>{{ doc.filename || doc.url }}</td>
            <td>{{ doc.source || 'web' }}</td>
            <td>{{ doc.chunk_count || (doc.content ? doc.content.length : 0) }}</td>
            <td>{{ new Date(doc.created_at).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
