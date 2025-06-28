'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChat = async () => {
    if (!query.trim()) return

    setLoading(true)
    try {
      const result = await axios.post(`${API_URL}/api/v1/chat`, {
        user_id: 'user_123',
        conversation_id: `conv_${Date.now()}`,
        text: query
      })
      setResponse(result.data.response.response || 'Resposta recebida')
    } catch (error) {
      setResponse('Erro ao conectar com o servidor')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            ENEM Agent System
          </h1>
          <p className="text-xl text-gray-600">
            Sistema inteligente de preparação para o ENEM
          </p>
        </header>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Faça sua pergunta:
            </label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={4}
              placeholder="Ex: Explique a Revolução Francesa..."
            />
          </div>

          <button
            onClick={handleChat}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:opacity-50"
          >
            {loading ? 'Processando...' : 'Enviar Pergunta'}
          </button>

          {response && (
            <div className="mt-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-800 mb-3">Resposta:</h3>
              <div className="text-gray-700 whitespace-pre-wrap">{response}</div>
            </div>
          )}
        </div>

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold text-gray-800 mb-2">💬 Chat Inteligente</h3>
            <p className="text-gray-600">Tire dúvidas sobre qualquer matéria do ENEM</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold text-gray-800 mb-2">📚 Plano de Estudos</h3>
            <p className="text-gray-600">Receba um cronograma personalizado</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold text-gray-800 mb-2">🎯 Questionários</h3>
            <p className="text-gray-600">Teste seus conhecimentos</p>
          </div>
        </div>
      </div>
    </div>
  )
}