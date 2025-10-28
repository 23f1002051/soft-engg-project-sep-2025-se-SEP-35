import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import ChatbotPage from './pages/ChatbotPage'
import { AuthProvider } from './context/AuthContext'
import DashboardHR from './pages/DashboardHR';
import DashboardJob from './pages/DashboardJob';

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/dashboard-hr" element={<DashboardHR />} />
            <Route path="/dashboard-job" element={<DashboardJob />} />
            <Route path="/register" element={<Register />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
          </Routes>
      </div>
    </AuthProvider>
  )
}