<!-- 📁 src/pages/NotFound.vue -->
<template>
    <div class="flex flex-col items-center justify-center h-[80vh] text-center">
      <h1 class="text-6xl font-bold text-error">404</h1>
      <p class="text-xl text-gray-500 mt-4">Không tìm thấy trang bạn yêu cầu 😢</p>
      <router-link to="/dashboard" class="btn btn-primary mt-6">Về trang chủ</router-link>
    </div>
  </template>
  