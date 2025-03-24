<template>
  <div class="fixed bottom-0 left-0 right-0 bg-black text-green-400 text-xs font-mono max-h-40 overflow-y-auto px-4 py-2 z-50 shadow-inner">
    <div v-for="(log, index) in logs" :key="index" class="whitespace-pre-line">
      {{ log }}
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { io } from 'socket.io-client'

const logs = ref([])
const socket = io('/ws')

onMounted(() => {
  socket.on('connect', () => {
    console.log('✅ Connected to log stream')
  })

  socket.on('log', (msg) => {
    logs.value.push(msg)
    if (logs.value.length > 100) logs.value.shift()
    setTimeout(() => {
      const el = document.querySelector('.log-terminal')
      if (el) el.scrollTop = el.scrollHeight
    }, 100)
  })
})
</script>

<style scoped>
</style>