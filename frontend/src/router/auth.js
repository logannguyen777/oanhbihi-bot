const TOKEN_KEY = 'authToken'

/**
 * Auth Guard - Chặn truy cập nếu chưa đăng nhập
 */
export default function AuthGuard(to, from, next) {
  if (isLoggedIn() || to.path === '/login') {
    next()
  } else {
    next('/login')
  }
}

/**
 * Lưu token vào localStorage
 * @param {string} token 
 */
export function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

/**
 * Xóa token khi logout
 */
export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

/**
 * Lấy token hiện tại từ localStorage
 * @returns {string|null}
 */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * Kiểm tra người dùng đã đăng nhập chưa
 * @returns {boolean}
 */
export function isLoggedIn() {
  return !!getToken()
}

/**
 * Đăng xuất người dùng, xóa token và chuyển hướng về trang Login
 * @param {import('vue-router').Router} router - đối tượng router của Vue
 */
export function logout(router) {
    clearToken()
    window.$toast?.showToast?.('👋 Đã đăng xuất thành công!', 'info')
    router.push('/login')
}