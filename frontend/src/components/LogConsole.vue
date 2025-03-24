<template>
    <div
      ref="logContainer"
      class="bg-[#1e1e1e] text-gray-200 font-mono text-[13px] h-[300px] overflow-y-auto rounded-lg border border-gray-600 shadow-inner px-4 py-3 select-text"
    >
      <div
        v-for="(line, index) in logs"
        :key="index"
        class="whitespace-pre-wrap leading-snug"
      >
        <span class="text-[#6A9955]">$</span> {{ line }}
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