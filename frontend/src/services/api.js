import axios from 'axios'

const instance = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

const API_BASE = '/api/auth'

export const login = async (email, password) => {
  const res = await axios.post(`${API_BASE}/login`, { email, password })
  return res.data
}

export const register = async (userData) => {
  const res = await axios.post(`${API_BASE}/register`, userData)
  return res.data
}

export const setToken = (token) => {
  localStorage.setItem('token', token)
}

export const getToken = () => {
  return localStorage.getItem('token')
}

export const axiosAuth = axios.create()
axiosAuth.interceptors.request.use(config => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default instance