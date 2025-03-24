<!-- 📁 src/components/Toast.vue -->
<template>
    <div v-if="visible" :class="['toast toast-top toast-end z-50', typeClass]">
      <div class="alert" :class="alertClass">
        <span>{{ message }}</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const visible = ref(false)
  const message = ref('')
  const type = ref('success') // success | error | info
  
  const showToast = (msg, toastType = 'success', duration = 2500) => {
    message.value = msg
    type.value = toastType
    visible.value = true
    setTimeout(() => {
      visible.value = false
    }, duration)
  }
  
  defineExpose({ showToast })
  
  const typeClass = {
    success: 'text-green-700',
    error: 'text-red-700',
    info: 'text-blue-700',
  }[type.value]
  
  const alertClass = {
    success: 'alert-success',
    error: 'alert-error',
    info: 'alert-info',
  }[type.value]
  </script>
  