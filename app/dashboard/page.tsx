'use client'

import { useState, useEffect, useRef } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

interface CurrentJob {
  job_id: string
  fornecedora_nome: string
  logs: string[]
  status: 'processing' | 'completed' | 'error'
}

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [fornecedoras, setFornecedoras] = useState<any[]>([])
  const [processingFornecedora, setProcessingFornecedora] = useState<string | null>(null)
  const [currentJob, setCurrentJob] = useState<CurrentJob | null>(null)
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null)
  const logsEndRef = useRef<HTMLDivElement>(null)
  const router = useRouter()
  const supabase = createClient()

  // API URL
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

  useEffect(() => {
    checkUser()
  }, [])

  useEffect(() => {
    // Auto-scroll para o final dos logs
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [currentJob?.logs])

  // Cleanup do polling quando desmontar
  useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval)
      }
    }
  }, [pollingInterval])

  async function checkUser() {
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      router.push('/login')
      return
    }

    setUser(user)
    setLoading(false)
    loadFornecedoras()
  }

  async function loadFornecedoras() {
    try {
      const response = await fetch(`${API_URL}/api/fornecedoras`)
      const data = await response.json()

      if (response.ok) {
        setFornecedoras(data.fornecedoras || [])
      }
    } catch (error) {
      console.error('Erro ao carregar fornecedoras:', error)
    }
  }

  async function handleLogout() {
    await supabase.auth.signOut()
    router.push('/login')
  }

  function iniciarPolling(jobId: string) {
    // Limpar polling anterior se existir
    if (pollingInterval) {
      clearInterval(pollingInterval)
    }

    // Polling a cada 2 segundos
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/api/status-processamento/${jobId}`)
        const data = await response.json()

        if (response.ok) {
          setCurrentJob({
            job_id: data.job_id,
            fornecedora_nome: data.fornecedora_nome,
            logs: data.logs,
            status: data.status
          })

          // Parar polling se concluído ou erro
          if (data.status === 'completed' || data.status === 'error') {
            clearInterval(interval)
            setPollingInterval(null)
            setProcessingFornecedora(null)

            if (data.status === 'completed') {
              setMessage(`${data.fornecedora_nome} processada com sucesso!`)
              // Limpar mensagem após 5 segundos
              setTimeout(() => setMessage(''), 5000)
            } else {
              setMessage(`Erro ao processar ${data.fornecedora_nome}: ${data.error}`)
            }
          }
        }
      } catch (error) {
        console.error('Erro ao consultar status:', error)
      }
    }, 2000) // A cada 2 segundos

    setPollingInterval(interval)
  }

  async function handleProcessarFornecedora(fornecedoraId: string, fornecedoraNome: string) {
    setProcessingFornecedora(fornecedoraId)
    setMessage(`Iniciando processamento de ${fornecedoraNome}...`)

    try {
      // Iniciar processamento
      const response = await fetch(`${API_URL}/api/processar-fornecedora/${fornecedoraId}`, {
        method: 'POST'
      })

      const data = await response.json()

      if (response.ok) {
        // Inicializar monitor
        setCurrentJob({
          job_id: data.job_id,
          fornecedora_nome: fornecedoraNome,
          logs: [],
          status: 'processing'
        })

        setMessage('')

        // Iniciar polling
        iniciarPolling(data.job_id)
      } else {
        setMessage(`Erro: ${data.error}`)
        setProcessingFornecedora(null)
      }
    } catch (error) {
      setMessage(`Erro ao processar ${fornecedoraNome}`)
      setProcessingFornecedora(null)
      console.error('Erro:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#000000]">
        <p className="text-white">Carregando...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#000000]">
      <header className="bg-[#005f46] shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <Image
                src="/logo-vora.png"
                alt="Vora Energia"
                width={120}
                height={48}
                className="h-12 w-auto"
              />
              <h1 className="text-2xl font-bold text-white">
                Leitor de Faturas de Gás
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-white text-sm">{user?.email}</span>
              <button
                onClick={handleLogout}
                className="bg-[#00f494] text-black px-4 py-2 rounded-md hover:bg-white transition-colors font-medium"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Monitor de Processamento em Tempo Real */}
        {currentJob && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-2xl font-bold mb-4" style={{ color: '#005f46' }}>
              Monitor de Processamento
            </h2>

            {/* Header com status */}
            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${
                    currentJob.status === 'processing' ? 'bg-yellow-500 animate-pulse' :
                    currentJob.status === 'completed' ? 'bg-green-500' :
                    'bg-red-500'
                  }`} />
                  <span className="font-bold text-lg text-gray-900">
                    {currentJob.fornecedora_nome}
                  </span>
                </div>
                <span className="text-sm text-gray-600 font-medium">
                  {currentJob.status === 'processing' ? '⏳ Processando...' :
                   currentJob.status === 'completed' ? '✅ Concluído' :
                   '❌ Erro'}
                </span>
              </div>
            </div>

            {/* Console de logs */}
            <div className="bg-black text-green-400 p-4 rounded-lg font-mono text-sm h-96 overflow-y-auto">
              {currentJob.logs.length === 0 ? (
                <div className="text-gray-500">Aguardando logs...</div>
              ) : (
                currentJob.logs.map((log, index) => (
                  <div key={index} className="mb-1 whitespace-pre-wrap">
                    {log}
                  </div>
                ))
              )}
              {currentJob.status === 'processing' && (
                <div className="mt-2 animate-pulse inline-block">▊</div>
              )}
              <div ref={logsEndRef} />
            </div>

            {/* Botão para fechar monitor (quando concluído ou erro) */}
            {(currentJob.status === 'completed' || currentJob.status === 'error') && (
              <button
                onClick={() => setCurrentJob(null)}
                className="mt-4 w-full bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 px-4 rounded-md transition-colors font-medium"
              >
                Fechar Monitor
              </button>
            )}
          </div>
        )}

        {/* Grid de Botões das Fornecedoras */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Fornecedoras
          </h2>
          <p className="text-gray-600 mb-4">
            Clique no botão da fornecedora para processar as faturas automaticamente
          </p>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {fornecedoras.map((fornecedora) => (
              <button
                key={fornecedora.id}
                onClick={() => handleProcessarFornecedora(fornecedora.id, fornecedora.nome)}
                disabled={processingFornecedora !== null}
                className={`px-4 py-3 rounded-md font-medium transition-colors ${
                  processingFornecedora === fornecedora.id
                    ? 'bg-yellow-500 text-white cursor-wait'
                    : 'bg-[#00f494] text-black hover:bg-[#005f46] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed'
                }`}
              >
                {processingFornecedora === fornecedora.id ? (
                  <span>Processando...</span>
                ) : (
                  fornecedora.nome
                )}
              </button>
            ))}
          </div>

          {fornecedoras.length === 0 && (
            <p className="text-gray-500 text-center py-4">
              Carregando fornecedoras...
            </p>
          )}
        </div>

        {/* Mensagem de feedback */}
        {message && !currentJob && (
          <div className={`p-4 rounded-md ${
            message.includes('Erro')
              ? 'bg-red-50 text-red-800 border border-red-200'
              : 'bg-green-50 text-green-800 border border-green-200'
          }`}>
            <p className="text-sm font-medium">{message}</p>
          </div>
        )}
      </main>
    </div>
  )
}
