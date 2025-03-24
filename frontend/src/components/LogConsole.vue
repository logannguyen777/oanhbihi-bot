<!-- src/components/ui/LogConsole.vue -->
<template>
    <div class="bg-black text-green-400 font-mono text-sm p-4 h-[300px] overflow-y-auto rounded-xl shadow-inner" ref="logContainer">
      <div v-for="(line, index) in logs" :key="index" class="whitespace-pre-wrap">
        {{ line }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, nextTick } from 'vue'
  
  const props = defineProps({ logs: Array })
  const logContainer = ref(null)
  
  watch(
    () => props.logs.length,
    async () => {
      await nextTick()
      if (logContainer.value) {
        logContainer.value.scrollTop = logContainer.value.scrollHeight
      }
    }
  )
  </script>
  