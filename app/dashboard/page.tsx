'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [message, setMessage] = useState('')
  const [faturas, setFaturas] = useState<any[]>([])
  const [fornecedoras, setFornecedoras] = useState<any[]>([])
  const [processingFornecedora, setProcessingFornecedora] = useState<string | null>(null)
  const router = useRouter()
  const supabase = createClient()

  // API URL - Altere para a URL do ngrok quando estiver usando
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

  useEffect(() => {
    checkUser()
  }, [])

  async function checkUser() {
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      router.push('/login')
      return
    }

    setUser(user)
    setLoading(false)
    loadFaturas()
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

  async function loadFaturas() {
    try {
      const response = await fetch(`${API_URL}/api/faturas`)
      const data = await response.json()

      if (response.ok) {
        setFaturas(data.faturas || [])
      }
    } catch (error) {
      console.error('Erro ao carregar faturas:', error)
    }
  }

  async function handleLogout() {
    await supabase.auth.signOut()
    router.push('/login')
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setMessage('')
    }
  }

  async function handleUpload() {
    if (!file) {
      setMessage('Selecione um arquivo primeiro')
      return
    }

    setUploading(true)
    setMessage('')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData
      })

      const data = await response.json()

      if (response.ok) {
        setMessage('Arquivo enviado com sucesso! Processando...')
        await handleProcess(data.filepath)
      } else {
        setMessage(`Erro: ${data.error}`)
      }
    } catch (error) {
      setMessage('Erro ao enviar arquivo. Verifique se a API está rodando.')
      console.error('Erro:', error)
    } finally {
      setUploading(false)
    }
  }

  async function handleProcess(filepath: string) {
    setProcessing(true)

    try {
      const response = await fetch(`${API_URL}/api/processar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filepath })
      })

      const data = await response.json()

      if (response.ok) {
        setMessage('Fatura processada com sucesso!')
        setFile(null)
        loadFaturas()
      } else {
        setMessage(`Erro ao processar: ${data.error}`)
      }
    } catch (error) {
      setMessage('Erro ao processar arquivo')
      console.error('Erro:', error)
    } finally {
      setProcessing(false)
    }
  }

  async function handleProcessarFornecedora(fornecedoraId: string, fornecedoraNome: string) {
    setProcessingFornecedora(fornecedoraId)
    setMessage(`Processando ${fornecedoraNome}...`)

    try {
      const response = await fetch(`${API_URL}/api/processar-fornecedora/${fornecedoraId}`, {
        method: 'POST'
      })

      const data = await response.json()

      if (response.ok) {
        setMessage(`${fornecedoraNome} processada com sucesso!`)
        loadFaturas()
      } else {
        setMessage(`Erro ao processar ${fornecedoraNome}: ${data.error}`)
      }
    } catch (error) {
      setMessage(`Erro ao processar ${fornecedoraNome}`)
      console.error('Erro:', error)
    } finally {
      setProcessingFornecedora(null)
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
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Upload de Faturas
          </h2>
          <p className="text-gray-600 mb-4">
            Envie arquivos PDF ou XML de faturas para processamento automático
          </p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Selecione o arquivo (PDF ou XML)
              </label>
              <input
                type="file"
                accept=".pdf,.xml"
                onChange={handleFileChange}
                disabled={uploading || processing}
                className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#00f494] focus:border-[#00f494] p-2"
              />
            </div>

            {file && (
              <div className="bg-gray-50 p-3 rounded-md">
                <p className="text-sm text-gray-700">
                  <span className="font-medium">Arquivo selecionado:</span> {file.name}
                </p>
                <p className="text-sm text-gray-500">
                  Tamanho: {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || uploading || processing}
              className="w-full bg-[#00f494] text-black py-3 px-4 rounded-md hover:bg-[#005f46] hover:text-white transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Enviando...' : processing ? 'Processando...' : 'Enviar e Processar'}
            </button>

            {message && (
              <div className={`p-4 rounded-md ${
                message.includes('Erro')
                  ? 'bg-red-50 text-red-800 border border-red-200'
                  : 'bg-green-50 text-green-800 border border-green-200'
              }`}>
                <p className="text-sm font-medium">{message}</p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Processar Fornecedoras
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

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-900">
              Faturas Processadas
            </h2>
            <button
              onClick={loadFaturas}
              className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md transition-colors"
            >
              Atualizar
            </button>
          </div>

          {faturas.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              Nenhuma fatura processada ainda
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Número NF
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      CNPJ Cliente
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Valor
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Data Emissão
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fornecedor
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {faturas.map((fatura) => (
                    <tr key={fatura.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {fatura.numero_nf}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {fatura.cnpj_cliente}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        R$ {fatura.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {fatura.volume.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(fatura.data_emissao).toLocaleDateString('pt-BR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {fatura.fornecedor}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
