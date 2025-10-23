
import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';


export default function Navbar() {

  return (
    <header className="sticky max-w-7xl mx-auto top-5 z-50">
      <div className="flex items-center justify-between h-20 rounded-3xl bg-white shadow px-6">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2">
          <img src="/favicon.ico" alt="HIREHERO" className="h-10 w-auto" />
          <span className="text-2xl font-bold text-[#013362]">HIREHERO</span>
        </Link>

        {/* Actions */}
        <div className="flex items-center gap-4">
          {/* Sign In or My Account */}
            <Link
              to="/"
              className="px-6 py-3 rounded-2xl text-blue-950 font-medium border border-gray-300 hover:bg-gray-50"
            >
              Login
            </Link>
          <Link
            to="/register"
            className="px-6 py-3 font-normal rounded-2xl bg-gradient-to-r from-[#013362] to-[#005193] text-white hover:bg-[#143d78]"
          >
            Register
          </Link>
        </div>
      </div>
    </header>
  );
}