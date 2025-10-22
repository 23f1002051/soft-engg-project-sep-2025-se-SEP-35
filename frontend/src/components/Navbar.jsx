import React from 'react'
import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()
  const links = [
    { to: '/', label: 'Dashboard' },
    { to: '/chatbot', label: 'Chatbot' },
    { to: '/login', label: 'Login' },
    { to: '/register', label: 'Register' }
  ]

  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 className="text-xl font-semibold text-gray-700">Recruitment System</h1>
        <div className="flex gap-4">
          {links.map(link => (
            <Link
              key={link.to}
              to={link.to}
              className={`text-sm font-medium ${location.pathname === link.to ? 'text-blue-600' : 'text-gray-600 hover:text-blue-600'}`}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}