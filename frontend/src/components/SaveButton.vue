<script setup>
import { ref } from 'vue'
import api from '@/router/api'

const props = defineProps({
  keyName: String,
  value: String,
})

const loading = ref(false)

const saveConfig = async () => {
  loading.value = true
  try {
    const res = await api.post(`/api/config?key=${props.keyName}&value=${props.value}`)
    if (res.status === 200) {
      window.$toast?.showToast?.(`✅ Đã lưu ${props.keyName}`, 'success') // ✅ TOAST nè
      window.log?.(`[SAVE] ${props.keyName} = ${props.value}`)            // ✅ LOG realtime nếu có
    }
  } catch (err) {
    window.$toast?.showToast?.(`❌ Lỗi khi lưu ${props.keyName}`, 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <button class="btn btn-sm btn-primary" @click="saveConfig" :disabled="loading">
    <span v-if="loading" class="loading loading-spinner loading-xs"></span>
    <span v-else>Lưu</span>
  </button>
</template>
