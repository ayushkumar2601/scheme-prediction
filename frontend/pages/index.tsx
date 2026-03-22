import { useState, useEffect } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import PredictionForm from '../components/PredictionForm'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'
import { PredictionRequest, PredictionResponse } from '../types/prediction'
import { predictPolicyImpact } from '../services/api'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<PredictionResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handlePrediction = async (request: PredictionRequest) => {
    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await predictPolicyImpact(request)
      setResults(response)
      toast.success('Prediction completed successfully!')
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Prediction failed'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setResults(null)
    setError(null)
  }

  return (
    <>
      <Head>
        <title>Aadhaar Policy Impact Prediction System</title>
        <meta name="description" content="Predict the impact of Aadhaar policy changes on enrollment and update volumes across India" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Aadhaar Policy Impact Prediction
                </h1>
                <p className="mt-2 text-gray-600">
                  Analyze the impact of policy changes on Aadhaar enrollment and updates
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-500">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Production Ready
                  </span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Prediction Form */}
            <div className="lg:col-span-4">
              <div className="sticky top-8">
                <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-6">
                    Policy Parameters
                  </h2>
                  <PredictionForm 
                    onSubmit={handlePrediction}
                    isLoading={isLoading}
                    onReset={handleReset}
                  />
                </div>
              </div>
            </div>

            {/* Results Area */}
            <div className="lg:col-span-8">
              {isLoading && (
                <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
                  <LoadingSpinner />
                </div>
              )}

              {error && (
                <div className="bg-white rounded-xl shadow-lg border border-red-200 p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">
                        Prediction Error
                      </h3>
                      <div className="mt-2 text-sm text-red-700">
                        <p>{error}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {results && !isLoading && (
                <ResultsDisplay results={results} />
              )}

              {!results && !isLoading && !error && (
                <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center">
                  <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
                    <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <h3 className="mt-4 text-lg font-medium text-gray-900">
                    Ready for Prediction
                  </h3>
                  <p className="mt-2 text-gray-500">
                    Configure your policy parameters and click "Generate Prediction" to analyze the impact.
                  </p>
                </div>
              )}
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center text-gray-500 text-sm">
              <p>© 2025 Aadhaar Policy Impact Prediction System. Built with Next.js and deployed on Vercel.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}