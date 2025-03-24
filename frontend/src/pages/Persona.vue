<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">🎀 Quản lý Bot Personas</h1>

    <div class="mb-4">
      <button class="btn btn-primary" @click="showModal = true">➕ Thêm Persona</button>
    </div>

    <div class="grid md:grid-cols-2 gap-4">
      <div v-for="p in personas" :key="p.name" class="bg-white rounded shadow p-4">
        <div class="font-bold">{{ p.name }} ({{ p.age }} tuổi)</div>
        <div class="italic text-sm text-gray-500 mb-2">{{ p.style }}</div>
        <div class="text-sm whitespace-pre-line border p-2 rounded bg-gray-50">{{ p.prompt }}</div>
        <button class="btn btn-xs btn-error mt-2" @click="deletePersona(p)">🗑️ Xoá</button>
      </div>
    </div>

    <!-- Modal -->
    <dialog id="persona_modal" class="modal" :open="showModal">
      <div class="modal-box">
        <h3 class="font-bold text-lg">➕ Thêm Bot Persona</h3>
        <div class="form-control mt-2">
          <label class="label">Tên</label>
          <input v-model="form.name" class="input input-bordered" />
        </div>
        <div class="form-control mt-2">
          <label class="label">Tuổi</label>
          <input type="number" v-model="form.age" class="input input-bordered" />
        </div>
        <div class="form-control mt-2">
          <label class="label">Phong cách</label>
          <input v-model="form.style" class="input input-bordered" />
        </div>
        <div class="form-control mt-2">
          <label class="label">Prompt</label>
          <textarea v-model="form.prompt" class="textarea textarea-bordered"></textarea>
        </div>
        <div class="modal-action">
          <button class="btn" @click="showModal = false">Huỷ</button>
          <button class="btn btn-primary" @click="createPersona">Lưu</button>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../router/api'

const personas = ref([])
const showModal = ref(false)

const form = ref({
  name: '',
  age: 18,
  style: '',
  prompt: ''
})

const loadPersonas = async () => {
  const res = await axios.get('/persona')
  personas.value = res.data
}

const createPersona = async () => {
  await axios.post('/persona', form.value)
  showModal.value = false
  await loadPersonas()
}

const deletePersona = async (p) => {
  await axios.delete('/persona/' + p.id)
  await loadPersonas()
}

onMounted(loadPersonas)
</script>