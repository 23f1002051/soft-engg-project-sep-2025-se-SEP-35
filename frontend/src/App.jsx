import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ChatbotPage from './pages/ChatbotPage'
import { AuthProvider } from './context/AuthContext'

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/register" element={<Register />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
          </Routes>
      </div>
    </AuthProvider>
  )
}