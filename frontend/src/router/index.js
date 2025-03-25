import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Login from '@/pages/Login.vue'
import NotFound from '@/pages/NotFound.vue'
import AuthGuard from './auth'
import { isLoggedIn } from './auth'


const routes = [
    {
      path: '/',
      redirect: '/dashboard',
      meta: { requiresAuth: true },
    },
    {
      path: '/',
      component: DefaultLayout,
      meta: { requiresAuth: true },
      beforeEnter: AuthGuard,
      children: [
        { path: 'dashboard', component: () => import('@/pages/Dashboard.vue') },
        { path: 'chat', component: () => import('@/pages/Chat.vue') },
        { path: 'settings', component: () => import('@/pages/Settings.vue') },
        { path: 'train', component: () => import('@/pages/Train.vue') },
        { path: 'admin-chat', component: () => import('@/pages/AdminChat.vue') },
      ]
    },
    {
      path: '/login',
      name: 'Login', // ✅ Fix ở đây
      component: Login,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound,
    },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !isLoggedIn()) {
      next({ name: 'Login' })
    } else {
      next()
    }
})

export default router
