// 📁 src/router/auth.js
export default function AuthGuard(to, from, next) {
    const token = localStorage.getItem('token')
    if (token || to.path === '/login') {
      next()
    } else {
      next('/login')
    }
  }
  