<template>
    <button class="btn btn-primary mt-3" :disabled="loading">
      <span v-if="loading" class="loading loading-spinner"></span>
      <slot v-else>💾 Lưu</slot>
    </button>
  </template>
  
  <script setup>
  defineProps({ loading: Boolean })
  </script>
  