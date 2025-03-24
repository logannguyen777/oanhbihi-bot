<template>
  <div id="app" class="min-h-screen bg-base-100 text-base-content">
    <RouterView />
    <GlobalLogConsole />
  </div>
</template>

<script setup>
import GlobalLogConsole from './components/GlobalLogConsole.vue'
</script>

<style>
/* Optional: custom scrollbars for log console */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: rgba(100, 100, 100, 0.5);
  border-radius: 6px;
}
</style>