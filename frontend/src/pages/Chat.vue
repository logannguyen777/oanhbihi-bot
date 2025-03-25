<template>
    <div class="max-w-2xl mx-auto mt-8 space-y-4">
      <h2 class="text-2xl font-bold text-primary mb-4">💬 Chat với Oanh Bihi</h2>
  
      <div class="flex gap-4 items-center">
        <label class="label cursor-pointer">
            <input type="radio" v-model="mode" value="rag-context" class="radio radio-sm checked:bg-primary" />
            <span class="ml-2">RAG + Context (mặc định)</span>
        </label>
        <label class="label cursor-pointer">
          <input type="radio" v-model="mode" value="rag" class="radio radio-sm checked:bg-primary" />
          <span class="ml-2">RAG</span>
        </label>
        <label class="label cursor-pointer">
          <input type="radio" v-model="mode" value="context" class="radio radio-sm checked:bg-primary" />
          <span class="ml-2">Có Context</span>
        </label>
      </div>
  
      <textarea v-model="message" placeholder="Nhập tin nhắn..." class="textarea textarea-bordered w-full" rows="3" />
  
      <button @click="sendMessage" class="btn btn-primary w-full" :disabled="loading">
        <span v-if="loading" class="loading loading-spinner"></span>
        <span v-else>Gửi tin nhắn</span>
      </button>
  
      <div v-if="reply" class="mt-4 p-4 bg-orange-100 rounded-lg text-gray-800">
        <strong>💬 Bot trả lời:</strong>
        <p class="mt-1 whitespace-pre-line">{{ reply }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '@/router/api'
  
  const message = ref('')
  const reply = ref('')
  const loading = ref(false)
  const mode = ref('rag-context') // 'rag' | 'context'
  
  const sendMessage = async () => {
    if (!message.value) return window.$toast.showToast('⚠️ Vui lòng nhập nội dung', 'info')
    loading.value = true
    reply.value = ''
  
    try {
        let res
        if (mode.value === 'rag') {
        res = await api.post('/api/chat-rag', { input_text: message.value })
        } else if (mode.value === 'context') {
        res = await api.post('/api/chat', {
            sender_id: 'admin',
            channel: 'web',
            message: message.value,
            session_id: null,
        })
        } else {
        // 👇 Mặc định: rag-context
        res = await api.post('/api/chat-rag-context', {
            sender_id: 'admin',
            channel: 'web',
            message: message.value,
            session_id: null,
        })
        }
  
      reply.value = res?.data?.reply || '🤖 Không có phản hồi từ bot!'
      window.$toast.showToast('✅ Bot đã phản hồi!', 'success')
    } catch (err) {
      window.$toast.showToast('❌ Lỗi khi gửi tin nhắn', 'error')
    } finally {
      loading.value = false
    }
  }
  </script>
  