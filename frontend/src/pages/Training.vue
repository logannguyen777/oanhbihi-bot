<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">🧠 Quản lý Dữ liệu Huấn luyện</h1>

    <div class="mb-4 flex gap-2 items-center">
      <input type="file" @change="handleFileUpload" class="file-input file-input-bordered" />
      <button class="btn btn-primary" @click="fetchData">🔄 Làm mới</button>
      <button class="btn btn-success" @click="runTrain">🏋️ Train Embedding</button>
    </div>

    <div class="overflow-x-auto">
      <table class="table w-full table-sm">
        <thead>
          <tr>
            <th>#</th>
            <th>URL</th>
            <th>Nội dung</th>
            <th>Đã Embedding?</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in pages" :key="row.id">
            <td>{{ idx + 1 }}</td>
            <td class="truncate max-w-[200px]">{{ row.url }}</td>
            <td class="text-sm max-w-[400px] whitespace-pre-line">{{ row.content.slice(0, 200) }}</td>
            <td>
              <span class="badge" :class="row.embedding ? 'badge-success' : 'badge-warning'">
                {{ row.embedding ? '✅ Có' : '⚠️ Chưa' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../router/api'
import { toast } from 'vue3-toastify'

const pages = ref([])

const fetchData = async () => {
  const res = await axios.get('/training/web-pages')
  pages.value = res.data
}

const runTrain = async () => {
  await axios.post('/training/train')
  toast.success('🏋️ Đã gửi lệnh train!')
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  await axios.post('/training/upload', formData)
  toast.success('📥 Upload thành công!')
  await fetchData()
}

onMounted(fetchData)
</script>