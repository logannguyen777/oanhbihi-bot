<template>
  <div class="max-w-3xl mx-auto space-y-10 py-6">
    <h2 class="text-2xl font-bold text-primary">⚙️ Cấu hình hệ thống</h2>

    <!-- MESSENGER CONFIG -->
    <section class="bg-white shadow rounded-lg p-4">
      <h3 class="text-lg font-semibold mb-2">📩 Messenger</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input v-model="messenger.pageToken" placeholder="Page Token" class="input input-bordered w-full" />
        <input v-model="messenger.verifyToken" placeholder="Verify Token" class="input input-bordered w-full" />
      </div>
      <button class="btn btn-primary mt-3" @click="saveMessenger" :disabled="loading">
        <span v-if="loading" class="loading loading-spinner"></span>
        <span v-else>Lưu Messenger</span>
      </button>
    </section>

    <!-- PERSONA CONFIG -->
    <section class="bg-white shadow rounded-lg p-4">
      <h3 class="text-lg font-semibold mb-2">🧍‍♀️ Persona (Tính cách Bot)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input v-model="persona.name" placeholder="Tên Bot" class="input input-bordered w-full" />
        <input v-model="persona.age" placeholder="Tuổi" class="input input-bordered w-full" />
        <input v-model="persona.gender" placeholder="Giới tính" class="input input-bordered w-full" />
        <input v-model="persona.tone" placeholder="Giọng điệu" class="input input-bordered w-full" />
        <input v-model="persona.style" placeholder="Phong cách" class="input input-bordered w-full" />
        <input v-model="persona.greeting" placeholder="Lời chào" class="input input-bordered w-full" />
      </div>
      <button class="btn btn-primary mt-3" @click="savePersona" :disabled="loading">
        <span v-if="loading" class="loading loading-spinner"></span>
        <span v-else>Lưu Persona</span>
      </button>
    </section>

    <!-- CRAWL CONFIG -->
    <section class="bg-white shadow rounded-lg p-4">
      <h3 class="text-lg font-semibold mb-2">🌐 Crawl dữ liệu web</h3>
      <div class="space-y-2">
        <textarea v-model="crawl.urls" placeholder="Danh sách URL (mỗi dòng 1 URL)" class="textarea textarea-bordered w-full"></textarea>
        <input v-model="crawl.fileTypes" placeholder="File Types (vd: pdf,docx)" class="input input-bordered w-full" />
        <input v-model="crawl.schedule" placeholder="Schedule (vd: daily, weekly)" class="input input-bordered w-full" />
      </div>
      <button class="btn btn-primary mt-3" @click="saveCrawl" :disabled="loading">
        <span v-if="loading" class="loading loading-spinner"></span>
        <span v-else>Lưu Crawl Config</span>
      </button>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/router/api'

const loading = ref(false)

const messenger = ref({ pageToken: '', verifyToken: '' })
const persona = ref({ name: '', age: '', gender: '', tone: '', greeting: '', style: '' })
const crawl = ref({ urls: '', fileTypes: '', schedule: '' })

const saveMessenger = async () => {
  loading.value = true
  try {
    await api.post('/api/config/messenger', messenger.value)
    window.$toast.showToast('✅ Lưu Messenger thành công!', 'success')
  } catch (e) {
    window.$toast.showToast('❌ Lỗi khi lưu Messenger!', 'error')
  } finally {
    loading.value = false
  }
}

const savePersona = async () => {
  loading.value = true
  try {
    await api.post('/api/config/persona', persona.value)
    window.$toast.showToast('✅ Lưu Persona thành công!', 'success')
  } catch (e) {
    window.$toast.showToast('❌ Lỗi khi lưu Persona!', 'error')
  } finally {
    loading.value = false
  }
}

const saveCrawl = async () => {
  loading.value = true
  try {
    const payload = {
      urls: crawl.value.urls.split('\n').filter(Boolean),
      fileTypes: crawl.value.fileTypes.split(',').map(x => x.trim()),
      schedule: crawl.value.schedule,
    }
    await api.post('/api/config/crawl', payload)
    window.$toast.showToast('✅ Lưu Crawl thành công!', 'success')
  } catch (e) {
    window.$toast.showToast('❌ Lỗi khi lưu Crawl!', 'error')
  } finally {
    loading.value = false
  }
}
</script>
