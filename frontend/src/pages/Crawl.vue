<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">🌐 Cấu hình Crawl Dữ Liệu</h1>

    <div class="mb-4">
      <button class="btn btn-primary" @click="showModal = true">➕ Thêm URL Crawl</button>
      <button class="btn btn-success ml-2" @click="runCrawl">🚀 Chạy Crawl</button>
    </div>

    <table class="table w-full">
      <thead>
        <tr>
          <th>Label</th>
          <th>URL</th>
          <th>Selector</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in crawls" :key="c.url">
          <td>{{ c.label }}</td>
          <td class="truncate max-w-[250px]">{{ c.url }}</td>
          <td>{{ c.selector }}</td>
          <td><button class="btn btn-xs btn-error" @click="deleteCrawl(c)">Xoá</button></td>
        </tr>
      </tbody>
    </table>

    <!-- Modal thêm mới -->
    <dialog id="crawl_modal" class="modal" :open="showModal">
      <div class="modal-box">
        <h3 class="font-bold text-lg">➕ Thêm cấu hình crawl</h3>
        <div class="form-control mt-2">
          <label class="label">Label</label>
          <input v-model="form.label" class="input input-bordered" />
        </div>
        <div class="form-control mt-2">
          <label class="label">URL</label>
          <input v-model="form.url" class="input input-bordered" />
        </div>
        <div class="form-control mt-2">
          <label class="label">CSS Selector</label>
          <input v-model="form.selector" class="input input-bordered" />
        </div>
        <div class="modal-action">
          <button class="btn" @click="showModal = false">Huỷ</button>
          <button class="btn btn-primary" @click="createCrawl">Lưu</button>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../router/api'
import { toast } from 'vue3-toastify'

const crawls = ref([])
const showModal = ref(false)
const form = ref({ url: '', selector: '', label: '' })

const loadCrawls = async () => {
  const res = await axios.get('/api/crawl')
  crawls.value = res.data
}

const createCrawl = async () => {
  await axios.post('/crawl', form.value)
  showModal.value = false
  toast.success('✅ Đã thêm URL crawl!')
  await loadCrawls()
}

const deleteCrawl = async (c) => {
  await axios.delete('/crawl/' + c.id)
  toast.success('🗑️ Đã xoá!')
  await loadCrawls()
}

const runCrawl = async () => {
  await axios.post('/crawl/run')
  toast.info('🚀 Đã chạy crawl, xem log realtime bên dưới!')
}

onMounted(loadCrawls)
</script>