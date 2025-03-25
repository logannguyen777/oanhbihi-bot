import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import Toast from '@/components/Toast.vue'

const app = createApp(App)
app.use(router)
app.mount('#app')

window.$toast = {
    showToast: (msg, type = 'info') => {
      // Nếu dùng thư viện toast thì gọi thư viện ở đây
      alert(`[${type.toUpperCase()}] ${msg}`) // 🚨 Tạm thời dùng alert
      alert(`[${type}] ${msg}`) 
    }
}

window.log = (msg) => {
    const logMsg = `[${new Date().toLocaleTimeString()}] ${msg}`
    console.log(logMsg)
  
    // nếu dùng WebSocket/console UI:
    const event = new CustomEvent('__log__', { detail: logMsg })
    window.dispatchEvent(event)
}
  