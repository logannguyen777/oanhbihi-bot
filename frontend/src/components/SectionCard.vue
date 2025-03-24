<template>
    <section class="bg-black shadow rounded-xl p-6 space-y-4">
      <h3 class="text-xl font-semibold text-gray-700">{{ title }}</h3>
      <slot />
    </section>
  </template>
  
  <script setup>
  defineProps({ title: String })
  </script>
  