import React, { useState } from 'react';

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '' });

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRegister = (e) => {
    e.preventDefault();
    alert(`Registering ${form.email}`);
  };

  return (
    <section className="min-h-[calc(100vh-5rem)] bg-[#F7F8FF] flex items-center justify-center">
      <div className="max-w-7xl w-full mx-auto grid md:grid-cols-2 rounded-3xl shadow-sm border border-gray-200 bg-white overflow-hidden">
        {/* ===== Left: Register Form ===== */}
        <section className="p-10 flex flex-col justify-center">
          {/* Header */}
          <div className="mb-10">
            <h1 className="text-3xl font-bold text-[#013362] flex items-center gap-2">
              <img src="/favicon.ico" alt="HIREHERO" className="w-8" /> Join HireHero
            </h1>
          </div>

        {/* Signup Form */}
        <form className="space-y-5">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-700">First Name</label>
              <input
                type="text"
                placeholder="Enter first name"
                className="w-full border border-gray-300 rounded-lg px-4 py-3 mt-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#005193]"
              />
            </div>
            <div>
              <label className="text-sm text-gray-700">Last Name</label>
              <input
                type="text"
                placeholder="Enter last name"
                className="w-full border border-gray-300 rounded-lg px-4 py-3 mt-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#005193]"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-700">Company Name</label>
              <input
                type="text"
                placeholder="Enter company name"
                className="w-full border border-gray-300 rounded-lg px-4 py-3 mt-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#005193]"
              />
            </div>
            <div>
              <label className="text-sm text-gray-700">Work Email</label>
              <input
                type="email"
                placeholder="Enter work email"
                className="w-full border border-gray-300 rounded-lg px-4 py-3 mt-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#005193]"
              />
            </div>
          </div>

          <div>
            <label className="text-sm text-gray-700">Select Your Role</label>
            <select
              className="w-full border border-gray-300 rounded-lg px-4 py-3 mt-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#005193]"
            >
              <option value="">Select role</option>
              <option value="hr">HR Professional</option>
              <option value="recruiter">Recruiter</option>
              <option value="manager">Hiring Manager</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-700">Password</label>
            <input
              type="password"
              placeholder="Create password"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 mt-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#005193]"
            />
          </div>

          {/* Terms Checkbox */}
          <div className="flex items-start text-sm text-gray-600">
            <input
              type="checkbox"
              className="accent-[#013362] mt-1 mr-2"
              required
            />
            <p>
              I agree to the{" "}
              <a href="#" className="text-[#005193] font-semibold hover:underline">
                Terms of Service
              </a>{" "}
              and{" "}
              <a href="#" className="text-[#005193] font-semibold hover:underline">
                Privacy Policy
              </a>
              .
            </p>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-[#013362] to-[#005193] text-white py-2.5 rounded-lg font-semibold hover:opacity-90 transition"
          >
            Create Account 🡢 
          </button>
        </form>


          <p className="text-center text-sm text-gray-500 mt-6">
            Already have an account?{' '}
            <a href="/login" className="text-[#005193] font-semibold hover:underline">
              Login
            </a>
          </p>
        </section>

        {/* ===== Right: Info Section ===== */}
        <section
          className="relative bg-[#013362] text-white p-10 flex flex-col justify-center overflow-hidden"
        >
          <div className="absolute inset-0 w-full h-full z-0">
            <div className="w-full h-full bg-cover bg-center" style={{ backgroundImage: "url('/background.jpg')" }}>
              <div className="w-full h-full bg-[#013362] bg-opacity-60"></div>
            </div>
          </div>
          <div className="relative z-10">
            <div className="max-w-md">
              <h2 className="text-3xl font-bold mb-6 leading-snug">
                AI Powered HR Management
              </h2>
              <ul className="space-y-4 text-md">
                <li className="flex items-center gap-2">
                  <img src="/check.svg" alt="check" className="w-10 h-8" /> Automated resume screening
                </li>
                <li className="flex items-center gap-2">
                  <img src="/check.svg" alt="check" className="w-10 h-8" /> Intelligent performance insights
                </li>
                <li className="flex items-center gap-2">
                  <img src="/check.svg" alt="check" className="w-10 h-8" /> Smart employee matching
                </li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </section>
  );
}