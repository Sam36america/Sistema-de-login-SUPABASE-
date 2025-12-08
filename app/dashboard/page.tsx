import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import LogoutButton from '@/components/LogoutButton'

export default async function DashboardPage() {
  const supabase = await createClient()

  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
            </div>
            <div className="flex items-center">
              <LogoutButton />
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Bem-vindo ao Sistema de Login!
            </h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-500">Email:</p>
                <p className="mt-1 text-lg text-gray-900">{user.email}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">ID do Usuário:</p>
                <p className="mt-1 text-sm text-gray-900 font-mono">{user.id}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Última atualização:</p>
                <p className="mt-1 text-sm text-gray-900">
                  {new Date(user.updated_at || '').toLocaleString('pt-BR')}
                </p>
              </div>
            </div>
            <div className="mt-6 p-4 bg-green-50 rounded-md">
              <p className="text-sm text-green-800">
                Sistema de autenticação funcionando corretamente! Você está logado e esta é uma área protegida.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
