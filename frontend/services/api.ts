import axios from 'axios'
import { PredictionRequest, PredictionResponse } from '../types/prediction'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:10000'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  timeout: 120000, // 2 minutes timeout for predictions
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    
    // Handle specific error cases
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout - the prediction is taking longer than expected')
    }
    
    if (error.response?.status === 500) {
      throw new Error('Server error - please try again later')
    }
    
    if (error.response?.status === 400) {
      throw new Error(error.response.data?.message || 'Invalid request parameters')
    }
    
    if (!error.response) {
      throw new Error('Network error - please check your connection')
    }
    
    return Promise.reject(error)
  }
)

/**
 * Get list of available states
 */
export const getStates = async (): Promise<string[]> => {
  try {
    const response = await api.get('/api/states')
    return response.data.states
  } catch (error) {
    console.error('Failed to fetch states:', error)
    // Return fallback list of major states
    return [
      'Andhra Pradesh', 'Bihar', 'Gujarat', 'Karnataka', 'Kerala',
      'Madhya Pradesh', 'Maharashtra', 'Rajasthan', 'Tamil Nadu',
      'Uttar Pradesh', 'West Bengal'
    ]
  }
}

/**
 * Generate policy impact prediction
 */
export const predictPolicyImpact = async (request: PredictionRequest): Promise<PredictionResponse> => {
  try {
    const response = await api.post('/api/predict', request)
    
    if (!response.data.success) {
      throw new Error(response.data.error || 'Prediction failed')
    }
    
    return response.data
  } catch (error: any) {
    console.error('Prediction failed:', error)
    
    // Re-throw with user-friendly message
    if (error.response?.data?.message) {
      throw new Error(error.response.data.message)
    }
    
    throw error
  }
}

/**
 * Get prediction by ID
 */
export const getPrediction = async (predictionId: number): Promise<any> => {
  try {
    const response = await api.get(`/api/predictions/${predictionId}`)
    
    if (!response.data.success) {
      throw new Error(response.data.error || 'Failed to fetch prediction')
    }
    
    return response.data.prediction
  } catch (error) {
    console.error('Failed to fetch prediction:', error)
    throw error
  }
}

/**
 * List recent predictions
 */
export const listPredictions = async (page: number = 1, limit: number = 10): Promise<any[]> => {
  try {
    const response = await api.get('/api/predictions', {
      params: { page, limit }
    })
    
    if (!response.data.success) {
      throw new Error(response.data.error || 'Failed to fetch predictions')
    }
    
    return response.data.predictions
  } catch (error) {
    console.error('Failed to fetch predictions:', error)
    throw error
  }
}

/**
 * Health check
 */
export const healthCheck = async (): Promise<any> => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

export default api