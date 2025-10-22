import React, { useState } from 'react'
import { askChatbot } from '../services/chatbotService'

export default function ChatbotWidget() {
  const [prompt, setPrompt] = useState('')
  const [reply, setReply] = useState('')

  const handleAsk = async () => {
    if (!prompt) return
    setReply('Thinking...')
    try {
      const res = await askChatbot(prompt)
      setReply(res)
    } catch {
      setReply('Error connecting to chatbot API')
    }
  }

  return (
    <div className="max-w-lg mx-auto mt-6 bg-white p-4 rounded-lg shadow">
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows="4"
        className="w-full border p-2 rounded"
        placeholder="Ask something about recruitment..."
      />
      <button
        onClick={handleAsk}
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Ask Chatbot
      </button>
      <div className="mt-4 p-3 bg-gray-100 rounded min-h-[80px] whitespace-pre-wrap">
        {reply}
      </div>
    </div>
  )
}