<template>
  <DefaultLayout />
  <Toast ref="toast" />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Toast from '@/components/Toast.vue'

const toast = ref(null)

onMounted(() => {
  window.$toast = toast.value
})
</script>