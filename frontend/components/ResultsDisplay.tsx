import { PredictionResponse } from '../types/prediction'
import SummaryCards from './SummaryCards'
import Charts from './Charts'
import RegionalImpactTable from './RegionalImpactTable'
import RiskAssessment from './RiskAssessment'

interface ResultsDisplayProps {
  results: PredictionResponse
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const { results: predictionResults, metadata } = results

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Prediction Results
            </h2>
            <p className="text-gray-600 mt-1">
              {metadata.policy_name} • {metadata.forecast_days} days forecast
            </p>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-500">Policy Date</div>
            <div className="text-lg font-semibold text-gray-900">
              {new Date(metadata.policy_date).toLocaleDateString()}
            </div>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <SummaryCards summary={predictionResults.summary} />

      {/* Charts */}
      <Charts 
        dailyImpact={predictionResults.daily_impact}
        regionalImpact={predictionResults.regional_impact}
        peakAnalysis={predictionResults.peak_analysis}
      />

      {/* Regional Impact Table */}
      <RegionalImpactTable 
        regionalData={predictionResults.regional_impact.top_10_states}
      />

      {/* Risk Assessment */}
      <RiskAssessment 
        riskData={predictionResults.risk_assessment}
        peakAnalysis={predictionResults.peak_analysis}
      />

      {/* Metadata */}
      <div className="bg-gray-50 rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Prediction Metadata
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <div className="text-gray-500">Compliance Level</div>
            <div className="font-medium">{Math.round(metadata.compliance_level * 100)}%</div>
          </div>
          <div>
            <div className="text-gray-500">Forecast Period</div>
            <div className="font-medium">{metadata.forecast_days} days</div>
          </div>
          <div>
            <div className="text-gray-500">Generated At</div>
            <div className="font-medium">
              {new Date(metadata.generated_at).toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-gray-500">Affected States</div>
            <div className="font-medium">
              {metadata.affected_states ? metadata.affected_states.length : 'All'}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}