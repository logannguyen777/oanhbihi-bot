<!-- 📁 src/layouts/DefaultLayout.vue -->
<template>
    <div class="drawer lg:drawer-open bg-base-100 min-h-screen">
      <input id="drawer-toggle" type="checkbox" class="drawer-toggle" />
      <div class="drawer-content">
        <label for="drawer-toggle" class="btn btn-primary m-2 lg:hidden">☰</label>
        <div class="p-4">
          <router-view />
        </div>
      </div>
      <div class="drawer-side border-r border-orange-200">
        <label for="drawer-toggle" class="drawer-overlay"></label>
        <Sidebar />
      </div>
    </div>
  </template>
  
  <script setup>
  import Sidebar from '@/components/Sidebar.vue'
  </script>
  