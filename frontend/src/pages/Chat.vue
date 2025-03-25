<template>
    <div class="max-w-3xl mx-auto p-6 space-y-6">
      <h2 class="text-2xl font-bold text-primary mb-4">💬 Chat với Oanh Bihi</h2>
  
      <!-- Chế độ -->
      <div class="flex flex-wrap gap-4">
        <label class="flex items-center gap-2">
          <input type="radio" v-model="mode" value="rag-context" class="radio radio-sm checked:bg-primary" />
          <span class="text-sm">RAG + Context</span>
        </label>
        <label class="flex items-center gap-2">
          <input type="radio" v-model="mode" value="rag" class="radio radio-sm checked:bg-primary" />
          <span class="text-sm">Chỉ RAG</span>
        </label>
        <label class="flex items-center gap-2">
          <input type="radio" v-model="mode" value="context" class="radio radio-sm checked:bg-primary" />
          <span class="text-sm">Chỉ Context</span>
        </label>
      </div>
  
      <!-- Vùng chat -->
      <div class="bg-base-100 border rounded-lg p-4 h-[500px] overflow-y-auto space-y-3 shadow-inner" ref="chatBox">
        <div
          v-for="(msg, idx) in chatHistory"
          :key="idx"
          :class="msg.role === 'user' ? 'chat chat-end' : 'chat chat-start'"
        >
          <div class="chat-image avatar">
            <div class="w-8 rounded-full">
              <img :src="msg.role === 'user' ? userAvatar : botAvatar" alt="avatar" />
            </div>
          </div>
          <div>
            <div
              class="chat-bubble"
              :class="msg.role === 'user' ? 'chat-bubble-primary' : 'chat-bubble-secondary'"
            >
              {{ msg.content }}
            </div>
            <div class="text-xs opacity-60 mt-1">
              {{ msg.role === 'user' }} • {{ formatTime(msg.timestamp) }}
            </div>
          </div>
        </div>
      </div>
  
      <!-- Nhập tin -->
      <div class="flex gap-2 items-end">
        <textarea
          v-model="message"
          @keydown.enter.exact.prevent="sendMessage"
          @keydown.enter.shift="() => {}"
          placeholder="Nhấn Enter để gửi, Shift+Enter để xuống dòng..."
          rows="2"
          class="textarea textarea-bordered flex-1 resize-none"
        />
        <button class="btn btn-primary" @click="sendMessage" :disabled="loading">
          <span v-if="loading" class="loading loading-spinner"></span>
          <span v-else>Gửi</span>
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue'
  import api from '@/router/api'
  
  const message = ref('')
  const chatHistory = ref([])
  const mode = ref('rag-context')
  const loading = ref(false)
  
  const botAvatar = 'https://i.imgur.com/BYkRZ5b.png'
  const userAvatar = 'https://i.imgur.com/xT5yF4M.png'
  
  const chatBox = ref(null)
  
  const scrollToBottom = async () => {
    await nextTick()
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  }
  
  const formatTime = (isoString) => {
    const date = new Date(isoString)
    return `${date.getHours().toString().padStart(2, '0')}:${date
      .getMinutes()
      .toString()
      .padStart(2, '0')}`
  }
  
  const sendMessage = async () => {
    if (!message.value.trim()) return window.$toast.showToast('⚠️ Nhập gì đi anh ơi!', 'info')
  
    const text = message.value.trim()
    const userMsg = { role: 'user', content: text, timestamp: new Date().toISOString() }
    chatHistory.value.push(userMsg)
    loading.value = true
    message.value = ''
    scrollToBottom()
  
    try {
      let res
      if (mode.value === 'rag') {
        res = await api.post('/api/chat-rag', { input_text: text })
      } else if (mode.value === 'context') {
        res = await api.post('/api/chat', {
          sender_id: 'admin',
          channel: 'web',
          message: text,
          session_id: null
        })
      } else {
        // rag-context
        const history = chatHistory.value.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
        res = await api.post('/api/chat-rag-context', {
          question: text,
          history
        })
      }
  
      const reply = res?.data?.reply || '🤖 Không có phản hồi từ bot!'
      chatHistory.value.push({ role: 'bot', content: reply, timestamp: new Date().toISOString() })
      window.$toast.showToast('✅ Oanh Bihi đã phản hồi!', 'success')
    } catch (err) {
      chatHistory.value.push({
        role: 'bot',
        content: '❌ Có lỗi xảy ra òi! Em xin lỗi anh nha...',
        timestamp: new Date().toISOString()
      })
      window.$toast.showToast('❌ Lỗi rồi đó anh ơi!', 'error')
    } finally {
      loading.value = false
      scrollToBottom()
    }
  }
  
  // WebSocket realtime (chưa gửi từ backend thì không nhận được đâu nha)
  onMounted(() => {
    const ws = new WebSocket(`ws://${window.location.host}/ws/logs`)
    ws.onmessage = (event) => {
      const msg = {
        role: 'bot',
        content: `[Log]: ${event.data}`,
        timestamp: new Date().toISOString()
      }
      chatHistory.value.push(msg)
      scrollToBottom()
    }
  })
  </script>
  