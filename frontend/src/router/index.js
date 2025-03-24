// 📁 src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import Chat from '@/pages/Chat.vue'
import Settings from '@/pages/Settings.vue'
import Train from '@/pages/Train.vue'
import AdminChat from '@/pages/AdminChat.vue'
import NotFound from '@/pages/NotFound.vue'
import AuthGuard from './auth'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard, beforeEnter: AuthGuard },
  { path: '/chat', component: Chat, beforeEnter: AuthGuard },
  { path: '/settings', component: Settings, beforeEnter: AuthGuard },
  { path: '/train', component: Train, beforeEnter: AuthGuard },
  { path: '/admin-chat', component: AdminChat, beforeEnter: AuthGuard },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
