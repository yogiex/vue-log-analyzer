import { ref, computed } from 'vue'

const USER_KEY = 'vue-la-user'

function getStoredUser() {
  try {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

const guestUser = {
  email: 'guest@demo.local',
  name: 'Guest',
  uid: 'guest-001',
  isLoggedIn: false,
}

const globalUser = ref(getStoredUser() || { ...guestUser })

export function useAuth() {
  const user = globalUser
  const isLoggedIn = computed(() => user.value.isLoggedIn === true)

  function login(credentials) {
    const userData = {
      email: credentials.email,
      name: credentials.email.split('@')[0],
      uid: 'user-' + Date.now(),
      isLoggedIn: true,
    }
    localStorage.setItem(USER_KEY, JSON.stringify(userData))
    user.value = userData
  }

  function logout() {
    localStorage.removeItem(USER_KEY)
    user.value = { ...guestUser }
  }

  function isAuthenticated() {
    return user.value.isLoggedIn === true
  }

  return { user, isLoggedIn, login, logout, isAuthenticated }
}
