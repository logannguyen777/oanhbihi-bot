<template>
  <div class="max-w-5xl mx-auto mt-10 space-y-6">
    <h2 class="text-2xl font-bold text-primary">🧠 Huấn luyện Oanh Bihi Bot</h2>

    <!-- Upload Files -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">📁 Upload tài liệu</h3>
      <input type="file" multiple @change="handleFileChange" class="file-input file-input-bordered w-full" />
      <button class="btn btn-secondary w-full" :disabled="!files.length || loading" @click="uploadFiles">
        <span v-if="loading" class="loading loading-spinner"></span>
        <span v-else>Upload tài liệu</span>
      </button>
    </div>

    <!-- Crawl URL -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">🌐 Crawl & Train từ URL</h3>
      <input v-model="url" type="text" placeholder="Nhập URL..." class="input input-bordered w-full" />
      <button class="btn btn-accent w-full mt-2" :disabled="!url" @click="crawlAndTrain">Crawl và Huấn luyện</button>
    </div>

    <!-- Select Model -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">🧠 Chọn mô hình embedding</h3>
      <select v-model="selectedModel" class="select select-bordered w-full">
        <option value="text-embedding-ada-002">OpenAI - Ada</option>
        <option value="all-MiniLM-L6-v2">MiniLM (local)</option>
        <option value="InstructorXL">Instructor XL (local)</option>
      </select>
    </div>

    <!-- Start Training -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">⚙️ Bắt đầu huấn luyện</h3>
      <button class="btn btn-primary w-full" :disabled="training" @click="startTraining">
        <span v-if="training" class="loading loading-spinner"></span>
        <span v-else>Huấn luyện ngay</span>
      </button>
    </div>

    <!-- Logs -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">📜 Log quá trình huấn luyện</h3>
      <LogConsole :logs="logs" />
    </div>

    <!-- Trained Documents Table -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">📊 Danh sách tài liệu đã huấn luyện</h3>
      <table class="table w-full">
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
            <td>{{ doc.filename }}</td>
            <td>{{ doc.source }}</td>
            <td>{{ doc.chunk_count }}</td>
            <td>{{ new Date(doc.created_at).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LogConsole from '@/components/LogConsole.vue'
import {
  uploadTrainingFiles,
  startTraining,
  getTrainedDocs,
  crawlUrl,
} from '@/router/api'

const files = ref([])
const loading = ref(false)
const training = ref(false)
const logs = ref([])
const url = ref('')
const selectedModel = ref('text-embedding-ada-002')
const trainedDocs = ref([])

const handleFileChange = (e) => {
  files.value = Array.from(e.target.files)
}

const uploadFiles = async () => {
  if (!files.value.length) return
  loading.value = true
  const formData = new FormData()
  files.value.forEach((file) => formData.append('files', file))

  try {
    await uploadTrainingFiles(formData)
    window.$toast.showToast('✅ Upload thành công!', 'success')
  } catch (err) {
    window.$toast.showToast('❌ Upload thất bại!', 'error')
  } finally {
    loading.value = false
  }
}

const startTrainingHandler = async () => {
  training.value = true
  try {
    await startTraining(selectedModel.value)
    window.$toast.showToast('✅ Huấn luyện hoàn tất!', 'success')
    await fetchTrainedDocs()
  } catch (err) {
    window.$toast.showToast('❌ Huấn luyện thất bại!', 'error')
  } finally {
    training.value = false
  }
}

const crawlAndTrain = async () => {
  try {
    await crawlUrl(url.value)
    await startTrainingHandler()
  } catch (err) {
    window.$toast.showToast('❌ Crawl thất bại!', 'error')
  }
}

const fetchTrainedDocs = async () => {
  const res = await getTrainedDocs()
  trainedDocs.value = res.data
}

onMounted(() => {
  const ws = new WebSocket(`ws://${window.location.host}/ws/logs`)
  ws.onmessage = (event) => {
    logs.value.push(event.data)
    setTimeout(() => {
      const logDiv = document.querySelector('.overflow-y-scroll')
      logDiv.scrollTop = logDiv.scrollHeight
    }, 100)
  }
  fetchTrainedDocs()
})
</script>