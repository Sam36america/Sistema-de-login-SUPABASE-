'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export default function TestSupabasePage() {
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const testConnection = async () => {
    setLoading(true)
    setResult(null)

    try {
      const supabase = createClient()

      // Testar se as variáveis de ambiente estão carregadas
      const url = process.env.NEXT_PUBLIC_SUPABASE_URL
      const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

      setResult({
        step: 'Variáveis de ambiente',
        url: url || 'NÃO ENCONTRADA',
        keyPrefix: key ? key.substring(0, 20) + '...' : 'NÃO ENCONTRADA',
        status: url && key ? '✅ OK' : '❌ ERRO'
      })

      // Testar conexão com Supabase
      const { data, error } = await supabase.auth.getSession()

      if (error) {
        setResult((prev: any) => ({
          ...prev,
          connectionTest: '❌ Erro de conexão',
          error: error.message
        }))
      } else {
        setResult((prev: any) => ({
          ...prev,
          connectionTest: '✅ Conexão OK',
          session: data.session ? 'Sessão ativa' : 'Sem sessão'
        }))
      }
    } catch (error: any) {
      setResult({
        error: '❌ ERRO CRÍTICO',
        message: error.message,
        name: error.name
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-4">🔍 Diagnóstico Supabase</h1>

        <button
          onClick={testConnection}
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:opacity-50 mb-6"
        >
          {loading ? 'Testando...' : 'Testar Conexão'}
        </button>

        {result && (
          <div className="bg-gray-50 p-4 rounded border">
            <h2 className="font-bold mb-2">Resultado:</h2>
            <pre className="text-sm whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded">
          <h3 className="font-bold mb-2">📋 Checklist:</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li>Verifique se o projeto Supabase está ativo em <a href="https://app.supabase.com/projects" target="_blank" className="text-blue-600 underline">app.supabase.com</a></li>
            <li>Confirme que a URL e chave no .env.local estão corretas</li>
            <li>Verifique se você tem autenticação por email/senha habilitada no Supabase</li>
            <li>Reinicie o servidor Next.js após mudar o .env.local</li>
          </ol>
        </div>
      </div>
    </div>
  )
}
