import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const uploadTrainingFiles = (formData) => {
    return axios.post('/training/upload', formData, {
        headers: {
        'Content-Type': 'multipart/form-data',
        },
    })
}

export const startTraining = () => axios.post('/training/start')
export const getTrainedDocs = () => axios.get('/training/docs')
export const crawlUrl = (url) => {
    return axios.post('/crawler/url', { url })
}
  

// CONFIG
export const getAllConfigs = () => api.get('/api/config')
export const getConfigByKey = (key) => api.get('/api/config', { params: { key } })
export const setConfigByKey = (key, value) => api.post('/api/config', null, { params: { key, value } }) 
export const saveSectionConfig = (endpoint, data) => api.post(endpoint, data)

// PERSONA
export const listPersonas = () => api.get('/api/persona')
export const createPersona = (data) => api.post('/api/persona', data)
export const deletePersona = (id) => api.delete(`/api/persona/${id}`)

// DASHBOARD
export const getCrawls = () => api.get('/api/crawl')
export const getWebPages = () => api.get('/api/training/web-pages')

export default api