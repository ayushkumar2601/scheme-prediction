import { AlertTriangle, Shield, CheckCircle, Clock } from 'lucide-react'

interface RiskData {
  high_impact_states: string[]
  states_at_risk: number
  risk_level: string
}

interface PeakAnalysis {
  peak_date: string
  peak_volume: number
  peak_enrolments: number
  peak_updates: number
}

interface RiskAssessmentProps {
  riskData: RiskData
  peakAnalysis: PeakAnalysis
}

export default function RiskAssessment({ riskData, peakAnalysis }: RiskAssessmentProps) {
  const getRiskIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return <AlertTriangle className="h-6 w-6 text-red-500" />
      case 'medium':
        return <Shield className="h-6 w-6 text-yellow-500" />
      case 'low':
        return <CheckCircle className="h-6 w-6 text-green-500" />
      default:
        return <Shield className="h-6 w-6 text-gray-500" />
    }
  }

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'border-red-200 bg-red-50'
      case 'medium':
        return 'border-yellow-200 bg-yellow-50'
      case 'low':
        return 'border-green-200 bg-green-50'
      default:
        return 'border-gray-200 bg-gray-50'
    }
  }

  const getRecommendations = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return [
          'Deploy additional staff to high-impact states',
          'Prepare backup systems and infrastructure',
          'Implement queue management systems',
          'Consider phased rollout to manage load',
          'Set up real-time monitoring dashboards'
        ]
      case 'medium':
        return [
          'Monitor system performance closely',
          'Prepare contingency plans for peak days',
          'Ensure adequate staff coverage',
          'Review infrastructure capacity'
        ]
      case 'low':
        return [
          'Standard monitoring procedures',
          'Regular system health checks',
          'Maintain current staffing levels'
        ]
      default:
        return ['Monitor system performance']
    }
  }

  const recommendations = getRecommendations(riskData.risk_level)

  return (
    <div className="space-y-6">
      {/* Risk Level Overview */}
      <div className={`bg-white rounded-xl shadow-lg border-2 ${getRiskColor(riskData.risk_level)} p-6`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getRiskIcon(riskData.risk_level)}
            <div>
              <h3 className="text-xl font-semibold text-gray-900">
                Risk Assessment: {riskData.risk_level}
              </h3>
              <p className="text-gray-600">
                {riskData.states_at_risk} states identified as high-impact
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-500">Peak Expected</div>
            <div className="text-lg font-semibold text-gray-900">
              {new Date(peakAnalysis.peak_date).toLocaleDateString()}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center space-x-2 mb-2">
              <AlertTriangle className="h-4 w-4 text-orange-500" />
              <span className="text-sm font-medium text-gray-700">High-Impact States</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {riskData.states_at_risk}
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center space-x-2 mb-2">
              <Clock className="h-4 w-4 text-blue-500" />
              <span className="text-sm font-medium text-gray-700">Peak Volume</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {peakAnalysis.peak_volume.toLocaleString()}
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="h-4 w-4 text-green-500" />
              <span className="text-sm font-medium text-gray-700">Risk Level</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {riskData.risk_level}
            </div>
          </div>
        </div>
      </div>

      {/* High-Impact States */}
      {riskData.high_impact_states.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            High-Impact States Requiring Attention
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {riskData.high_impact_states.map((state) => (
              <div
                key={state}
                className="bg-red-50 border border-red-200 rounded-lg p-3 text-center"
              >
                <div className="text-sm font-medium text-red-800">
                  {state}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">
          Recommended Actions
        </h4>
        <div className="space-y-3">
          {recommendations.map((recommendation, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 mt-1">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
              <div className="text-sm text-gray-700">
                {recommendation}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Timeline Alert */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-start space-x-3">
          <Clock className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-blue-900 mb-1">
              Peak Impact Timeline
            </h4>
            <p className="text-sm text-blue-800">
              Maximum impact is expected on{' '}
              <span className="font-semibold">
                {new Date(peakAnalysis.peak_date).toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </span>
              {' '}with approximately{' '}
              <span className="font-semibold">
                {peakAnalysis.peak_volume.toLocaleString()}
              </span>
              {' '}people affected. Plan resource allocation accordingly.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}