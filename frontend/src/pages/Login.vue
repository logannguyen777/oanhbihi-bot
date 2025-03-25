<template>
    <div class="min-h-screen flex items-center justify-center bg-base-100">
      <div class="w-full max-w-sm p-6 bg-white rounded-2xl shadow-md">
        <h2 class="text-2xl font-bold mb-4 text-center text-primary">Đăng nhập</h2>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <input v-model="username" type="text" placeholder="Tên đăng nhập" class="input input-bordered w-full" required />
          <input v-model="password" type="password" placeholder="Mật khẩu" class="input input-bordered w-full" required />
  
          <button class="btn btn-primary w-full" type="submit" :disabled="loading">
            <span v-if="loading" class="loading loading-spinner"></span>
            <span v-else>Đăng nhập</span>
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/router/api'
  import { saveToken } from '@/router/auth'

  // Nếu dùng vue-sonner thì import:
  // import { toast } from 'vue-sonner'
  
  const username = ref('')
  const password = ref('')
  const loading = ref(false)
  const router = useRouter()
  
  const handleLogin = async () => {
    loading.value = true
    try {
      const res = await api.post('/api/auth/login', {
        username: username.value,
        password: password.value,
      })
  
      if (res.status === 200 && res.data.token) {
        saveToken(res.data.token) // ✅ đúng chuẩn
        window.$toast?.showToast?.('✅ Đăng nhập thành công!', 'success')
        router.push('/dashboard')
      } else {
        // toast.error('❌ Đăng nhập thất bại')
        window.$toast?.showToast?.('❌ Đăng nhập thất bại', 'error')
      }
    } catch (err) {
      // toast.error('❌ Sai tên đăng nhập hoặc mật khẩu')
      window.$toast?.showToast?.('❌ Sai tên đăng nhập hoặc mật khẩu', 'error')
    } finally {
      loading.value = false
    }
  }
  </script>
  