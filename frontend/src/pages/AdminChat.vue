<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
    <!-- User List -->
    <div class="bg-white shadow rounded-lg p-4">
      <h2 class="text-lg font-bold mb-2 text-primary">👥 Người dùng</h2>
      <ul class="space-y-2 max-h-[400px] overflow-y-auto">
        <li v-for="user in users" :key="user.user_id">
          <button
            @click="selectUser(user.user_id)"
            class="btn btn-sm w-full"
            :class="{ 'btn-primary': user.user_id === selectedUserId }"
          >
            👤 User {{ user.user_id }}
          </button>
        </li>
      </ul>
    </div>

    <!-- Chat Content -->
    <div class="col-span-2 bg-white shadow rounded-lg p-4">
      <h2 class="text-lg font-bold text-primary">💬 Lịch sử chat</h2>

      <div v-if="loading" class="mt-4"><LoadingSpinner /></div>

      <div v-else-if="messages.length" class="space-y-2 mt-3 max-h-[300px] overflow-y-auto">
        <div v-for="msg in messages" :key="msg.id" class="chat chat-start">
          <div class="chat-bubble text-left">{{ msg.message }}</div>
        </div>
      </div>
      <p v-else class="text-sm text-gray-500 mt-4">Chưa có cuộc trò chuyện nào...</p>

      <!-- Reply -->
      <div v-if="selectedUserId" class="mt-4">
        <textarea
          v-model="adminReply"
          placeholder="Trả lời người dùng..."
          class="textarea textarea-bordered w-full"
        />
        <div class="flex gap-2 mt-2">
          <button class="btn btn-primary" @click="sendReply" :disabled="!adminReply">Gửi trả lời</button>
          <button class="btn btn-warning" @click="toggleBot">🔁 Bật/Tắt Bot</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/router/api'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const users = ref([])
const selectedUserId = ref(null)
const messages = ref([])
const adminReply = ref('')
const loading = ref(false)

const loadUsers = async () => {
  try {
    const res = await api.get('/api/admin/conversations')
    users.value = res.data || []
  } catch {
    window.$toast.showToast('❌ Không thể load danh sách người dùng', 'error')
  }
}

const selectUser = async (userId) => {
  selectedUserId.value = userId
  messages.value = []
  loading.value = true
  try {
    const res = await api.get(`/api/admin/conversations/${userId}`)
    messages.value = res.data || []
  } catch {
    window.$toast.showToast('❌ Không load được lịch sử chat', 'error')
  } finally {
    loading.value = false
  }
}

const sendReply = async () => {
  if (!selectedUserId.value || !adminReply.value) return
  try {
    await api.post('/api/admin/reply', {
      user_id: selectedUserId.value,
      message: adminReply.value,
    })
    window.$toast.showToast('✅ Đã gửi trả lời', 'success')
    adminReply.value = ''
    await selectUser(selectedUserId.value)
  } catch {
    window.$toast.showToast('❌ Không gửi được tin nhắn', 'error')
  }
}

const toggleBot = async () => {
  try {
    await api.post('/api/admin/toggle-bot', {
      user_id: selectedUserId.value,
    })
    window.$toast.showToast('✅ Đã bật/tắt bot cho user', 'success')
  } catch {
    window.$toast.showToast('❌ Không thể toggle bot', 'error')
  }
}

onMounted(() => {
  loadUsers()
})
</script>
