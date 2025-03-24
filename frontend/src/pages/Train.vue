<template>
  <div class="max-w-xl mx-auto mt-10 space-y-6">
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

    <!-- Start Training -->
    <div class="bg-white rounded-lg shadow p-4 space-y-3">
      <h3 class="text-lg font-semibold">⚙️ Bắt đầu huấn luyện</h3>
      <button class="btn btn-primary w-full" :disabled="training" @click="startTraining">
        <span v-if="training" class="loading loading-spinner"></span>
        <span v-else>Huấn luyện ngay</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/router/api'

const files = ref([])
const loading = ref(false)
const training = ref(false)

const handleFileChange = (e) => {
  files.value = Array.from(e.target.files)
}

const uploadFiles = async () => {
  if (!files.value.length) return
  loading.value = true
  const formData = new FormData()
  files.value.forEach((file) => formData.append('files', file))

  try {
    await api.post('/api/train/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    window.$toast.showToast('✅ Upload thành công!', 'success')
  } catch (err) {
    window.$toast.showToast('❌ Upload thất bại!', 'error')
  } finally {
    loading.value = false
  }
}

const startTraining = async () => {
  training.value = true
  try {
    await api.post('/api/train/start')
    window.$toast.showToast('✅ Huấn luyện hoàn tất!', 'success')
  } catch (err) {
    window.$toast.showToast('❌ Huấn luyện thất bại!', 'error')
  } finally {
    training.value = false
  }
}
</script>
