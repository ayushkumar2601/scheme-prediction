import { useState, useEffect } from 'react'
import DatePicker from 'react-datepicker'
import Select from 'react-select'
import { PredictionRequest } from '../types/prediction'
import { getStates } from '../services/api'
import 'react-datepicker/dist/react-datepicker.css'

interface PredictionFormProps {
  onSubmit: (request: PredictionRequest) => void
  isLoading: boolean
  onReset: () => void
}

interface StateOption {
  value: string
  label: string
}

export default function PredictionForm({ onSubmit, isLoading, onReset }: PredictionFormProps) {
  const [policyName, setPolicyName] = useState('')
  const [policyDate, setPolicyDate] = useState<Date>(new Date())
  const [forecastDays, setForecastDays] = useState(60)
  const [complianceLevel, setComplianceLevel] = useState(80)
  const [selectedStates, setSelectedStates] = useState<StateOption[]>([])
  const [availableStates, setAvailableStates] = useState<StateOption[]>([])
  const [loadingStates, setLoadingStates] = useState(true)

  useEffect(() => {
    loadStates()
  }, [])

  const loadStates = async () => {
    try {
      const states = await getStates()
      const stateOptions = states.map(state => ({
        value: state,
        label: state
      }))
      setAvailableStates(stateOptions)
    } catch (error) {
      console.error('Failed to load states:', error)
    } finally {
      setLoadingStates(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    const request: PredictionRequest = {
      policy_name: policyName || `Policy ${policyDate.toISOString().split('T')[0]}`,
      policy_date: policyDate.toISOString().split('T')[0],
      forecast_days: forecastDays,
      compliance_level: complianceLevel / 100,
      affected_states: selectedStates.length > 0 ? selectedStates.map(s => s.value) : undefined
    }

    onSubmit(request)
  }

  const handleReset = () => {
    setPolicyName('')
    setPolicyDate(new Date())
    setForecastDays(60)
    setComplianceLevel(80)
    setSelectedStates([])
    onReset()
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Policy Name */}
      <div>
        <label htmlFor="policyName" className="block text-sm font-medium text-gray-700 mb-2">
          Policy Name
        </label>
        <input
          type="text"
          id="policyName"
          value={policyName}
          onChange={(e) => setPolicyName(e.target.value)}
          placeholder="e.g., New Aadhaar Update Policy"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Policy Date */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Policy Implementation Date
        </label>
        <DatePicker
          selected={policyDate}
          onChange={(date: Date) => setPolicyDate(date)}
          minDate={new Date()}
          dateFormat="yyyy-MM-dd"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Forecast Days */}
      <div>
        <label htmlFor="forecastDays" className="block text-sm font-medium text-gray-700 mb-2">
          Forecast Period (Days)
        </label>
        <select
          id="forecastDays"
          value={forecastDays}
          onChange={(e) => setForecastDays(Number(e.target.value))}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value={30}>30 days</option>
          <option value={60}>60 days</option>
          <option value={90}>90 days</option>
          <option value={120}>120 days</option>
          <option value={180}>180 days</option>
        </select>
      </div>

      {/* Compliance Level */}
      <div>
        <label htmlFor="complianceLevel" className="block text-sm font-medium text-gray-700 mb-2">
          Expected Compliance Level: {complianceLevel}%
        </label>
        <input
          type="range"
          id="complianceLevel"
          min="0"
          max="100"
          step="5"
          value={complianceLevel}
          onChange={(e) => setComplianceLevel(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>

      {/* Affected States */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Affected States (Optional)
        </label>
        <Select
          isMulti
          value={selectedStates}
          onChange={(newValue) => setSelectedStates(newValue as StateOption[])}
          options={availableStates}
          isLoading={loadingStates}
          placeholder="Select states (leave empty for all states)"
          className="react-select-container"
          classNamePrefix="react-select"
          styles={{
            control: (base) => ({
              ...base,
              borderColor: '#d1d5db',
              '&:hover': {
                borderColor: '#3b82f6'
              }
            }),
            multiValue: (base) => ({
              ...base,
              backgroundColor: '#dbeafe'
            }),
            multiValueLabel: (base) => ({
              ...base,
              color: '#1e40af'
            })
          }}
        />
        <p className="text-xs text-gray-500 mt-1">
          Leave empty to analyze impact across all states
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-3 pt-4">
        <button
          type="submit"
          disabled={isLoading}
          className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating...
            </div>
          ) : (
            'Generate Prediction'
          )}
        </button>
        
        <button
          type="button"
          onClick={handleReset}
          disabled={isLoading}
          className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Reset
        </button>
      </div>
    </form>
  )
}