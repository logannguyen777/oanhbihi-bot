<template>
    <div class="max-w-3xl mx-auto p-6 space-y-6">
      <h2 class="text-2xl font-bold text-primary mb-4">💬 Chat với DNU - FTA</h2>
  
      <!-- Chế độ chọn -->
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
      <div class="bg-base-100 border rounded-lg p-4 h-[500px] overflow-y-auto space-y-3" ref="chatContainer">
        <div v-for="(msg, index) in chatLog" :key="index" class="flex items-start gap-2"
          :class="{ 'justify-end flex-row-reverse': msg.from === 'user' }">
          <img
            :src="msg.from === 'bot' ? botAvatar : userAvatar"
            class="w-8 h-8 rounded-full"
            :alt="msg.from === 'bot' ? 'DNU-FTA' : 'Bạn'"
          />
          <div class="space-y-1">
            <div class="text-xs text-gray-500">{{ msg.from === 'bot' ? 'DNU-FTA' : 'Bạn' }} • {{ msg.timestamp }}</div>
            <div class="p-3 rounded-2xl text-sm whitespace-pre-wrap max-w-[300px]" :class="{
              'bg-blue-500 text-white': msg.from === 'user',
              'bg-gray-100 text-gray-800': msg.from === 'bot',
              'bg-red-100 text-red-700': msg.from === 'error'
            }">
              {{ msg.text }}
            </div>
          </div>
        </div>
  
        <div v-if="isLoading" class="text-center text-sm text-gray-500 mt-2 animate-pulse">
          Đang gửi câu hỏi cho DNU-FTA ... ⏳
        </div>
      </div>
  
      <!-- Nhập tin nhắn -->
      <div class="flex gap-2">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          class="input input-bordered w-full"
          placeholder="Nhập câu hỏi và nhấn Enter..."
        />
        <button @click="sendMessage" class="btn btn-primary" :disabled="isLoading">Gửi</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue'
  import api from '@/router/api'
  
  const mode = ref('rag-context')
  const isLoading = ref(false)
  const sessionId = ref(Date.now().toString())
  const chatLog = ref([])
  const userInput = ref('')
  const chatContainer = ref(null)
  
  const userAvatar = 'https://api.dicebear.com/7.x/thumbs/svg?seed=user'
  const botAvatar = '/logo.png'
  
  // WebSocket nhận log từ backend
  const logs = ref([])
  let ws = null
  
  onMounted(() => {
    ws = new WebSocket('ws://localhost:8000/ws/logs')
    ws.onmessage = (event) => {
      logs.value.push(event.data)
      console.log("📡 Log:", event.data)
    }
  })
  
  function getTimeNow() {
    return new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
  }
  
  async function sendMessage() {
    if (!userInput.value.trim()) return
    const text = userInput.value.trim()
    userInput.value = ''
    chatLog.value.push({ from: 'user', text, timestamp: getTimeNow() })
  
    await nextTick(() => {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    })
  
    isLoading.value = true
    try {
      let endpoint = '/api/chat'
      if (mode.value === 'rag') endpoint = '/api/chat-rag'
      else if (mode.value === 'rag-context') endpoint = '/api/chat-rag-context'
  
      const payload = {
        sender_id: 'user-123',
        channel: 'web',
        message: text,
        session_id: sessionId.value,
      }
  
      const res = await api.post(endpoint, payload)
      const botReply = res.data.reply || res.data.message || '🤖 Không có phản hồi'
      chatLog.value.push({ from: 'bot', text: botReply, timestamp: getTimeNow() })
      //alert('Đã gửi câu hỏi 🎯')
    } catch (err) {
      console.error("❌ Chat API error:", err)
      chatLog.value.push({ from: 'error', text: 'Có lỗi xảy ra khi gửi câu hỏi!', timestamp: getTimeNow() })
      //alert('Oanh Bihi đang bận 😢')
    } finally {
      isLoading.value = false
      await nextTick(() => {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      })
    }
  }
  </script>
  