// src/router/api.js

import axios from 'axios'

// Khởi tạo axios instance chung
const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
})

// Gắn token tự động nếu có
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Các hàm API dùng chung instance `api`
export const getAllConfigs = () => api.get('/api/config')
export const setConfig = (key, value) => api.post('/api/config', null, { params: { key, value } })

export default api
