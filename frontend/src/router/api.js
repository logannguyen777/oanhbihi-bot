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

// Các hàm gọi API chuẩn hóa
export const getAllConfigs = () => api.get('/api/config')
export const setConfig = (key, value) => api.post('/api/config', null, { params: { key, value } })

export const uploadTrainingFiles = (formData) =>
  api.post('/api/train/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const startTraining = (model) =>
  api.post('/api/train/start', { model })

export const getTrainedDocs = () =>
  api.get('/api/train/docs')

export const crawlUrl = (url) =>
  api.post('/api/crawl', { url })

export default api