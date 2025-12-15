'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'error' | 'success'; text: string } | null>(null)
  const router = useRouter()
  const supabase = createClient()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      // Verificar se as credenciais do Supabase estão configuradas
      const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
      const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

      if (!supabaseUrl || !supabaseKey) {
        throw new Error('Configuração do Supabase não encontrada. Verifique o arquivo .env.local')
      }

      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) {
        // Mensagens de erro mais amigáveis
        if (error.message.includes('Invalid login credentials')) {
          throw new Error('Email ou senha incorretos')
        }
        if (error.message.includes('Email not confirmed')) {
          throw new Error('Email não confirmado. Verifique sua caixa de entrada')
        }
        throw error
      }

      if (data.user) {
        setMessage({
          type: 'success',
          text: 'Login realizado com sucesso!',
        })
        router.push('/dashboard')
        router.refresh()
      }
    } catch (error: any) {
      console.error('Erro de login:', error)

      // Tratamento específico para erro de rede
      if (error.message === 'Failed to fetch' || error.name === 'TypeError') {
        setMessage({
          type: 'error',
          text: 'Erro de conexão. Verifique sua internet ou se o Supabase está configurado corretamente.',
        })
      } else {
        setMessage({
          type: 'error',
          text: error.message || 'Erro ao fazer login',
        })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#000000]">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-md">
        <div className="flex flex-col items-center">
          <Image
            src="/logo-vora.png"
            alt="Vora Energia"
            width={200}
            height={80}
            className="mb-6"
            priority
            unoptimized
          />
          <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900">
            Leitor faturas de gás
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-[#00f494] focus:border-[#00f494] focus:z-10 sm:text-sm"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Senha
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-[#00f494] focus:border-[#00f494] focus:z-10 sm:text-sm"
                placeholder="Senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {message && (
            <div
              className={`rounded-md p-4 ${
                message.type === 'error' ? 'bg-red-50 text-red-800' : 'bg-green-50 text-green-800'
              }`}
            >
              <p className="text-sm">{message.text}</p>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-black bg-[#00f494] hover:bg-[#005f46] hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#00f494] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </div>

          <div className="text-center">
            <Link href="/signup" className="text-sm text-[#00f494] hover:text-[#005f46] font-medium transition-colors">
              Não tem uma conta? Cadastre-se
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
