import axios from 'axios'
import { getToken, clearToken } from './auth'


const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || 'https://backend.fta.thefirst.ai',
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

export const uploadTrainFiles = (formData) => api.post('/api/train/upload', formData)
export const startTraining = () => api.post('/api/train/start')
export const getTrainedDocs = () => api.get('/api/training/docs')

export const crawlUrl = (data) => {
    return api.post('/api/crawl', data)
}

export const crawlInstantUrl = (url) => {
    return api.post('/api/crawl/instant', {
      url: url,
      selector: 'body',
      label: 'Từ Settings'
    })
}

// CONFIG
export const getAllConfigs = () => api.get('/api/config')
export const getConfigByKey = (key) => api.get('/api/config', { params: { key } })
export const setConfigByKey = (key, value) => api.post('/api/config', null, { params: { key, value } }) 
export const saveSectionConfig = (endpoint, data) => api.post(endpoint, data)

export const getFacebookPages = (code, state) => axios.get(`/facebook/oauth/callback?code=${code}&state=${state}`)
export const connectFacebookPage = (data) => axios.post(`/api/facebook/pages`, data)


// DASHBOARD
export const getCrawls = () => api.get('/api/crawl')
export const getWebPages = () => api.get('/api/train/web-pages')

export default api