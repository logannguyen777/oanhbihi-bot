import axios from 'axios'
import { getToken, clearToken } from './auth'


const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      clearToken()
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

// ...original API methods remain unchanged
export const uploadTrainingFiles = (formData) => {
    return api.post('/api/train/upload', formData, {
        headers: {
        'Content-Type': 'multipart/form-data',
        },
    })
}

export const startTraining = () => api.post('/api/train/start')
export const getTrainedDocs = () => api.get('/api/train/web-pages')
export const crawlUrl = (url) => {
    return api.post('/api/crawl', { url })
}
  
// CONFIG
export const getAllConfigs = () => api.get('/api/config')
export const getConfigByKey = (key) => api.get('/api/config', { params: { key } })
export const setConfigByKey = (key, value) => api.post('/api/config', null, { params: { key, value } }) 
export const saveSectionConfig = (endpoint, data) => api.post(endpoint, data)


// DASHBOARD
export const getCrawls = () => api.get('/api/crawl')
export const getWebPages = () => api.get('/api/train/web-pages')

export default api