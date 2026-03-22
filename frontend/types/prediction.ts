export interface PredictionRequest {
  policy_name?: string
  policy_date: string
  forecast_days: number
  compliance_level: number
  affected_states?: string[]
}

export interface PredictionResponse {
  success: boolean
  results: PredictionResults
  metadata: PredictionMetadata
}

export interface PredictionResults {
  summary: SummaryData
  daily_impact: DailyImpact[]
  regional_impact: RegionalImpact
  peak_analysis: PeakAnalysis
  risk_assessment: RiskAssessment
}

export interface SummaryData {
  total_people_affected: number
  total_enrolment_impact: number
  total_update_impact: number
  average_daily_impact: number
  policy_date: string
  forecast_days: number
}

export interface DailyImpact {
  date: string
  enrolment_impact: number
  update_impact: number
  total_impact: number
}

export interface RegionalImpact {
  by_state: RegionalData[]
  top_10_states: RegionalData[]
  total_impact: Record<string, number>
  enrolment_impact: Record<string, number>
  update_impact: Record<string, number>
}

export interface RegionalData {
  state: string
  enrolment_impact: number
  update_impact: number
  total_impact: number
}

export interface PeakAnalysis {
  peak_date: string
  peak_volume: number
  peak_enrolments: number
  peak_updates: number
}

export interface RiskAssessment {
  high_impact_states: string[]
  states_at_risk: number
  risk_level: string
}

export interface PredictionMetadata {
  policy_date: string
  forecast_days: number
  compliance_level: number
  policy_name: string
  affected_states?: string[]
  generated_at: string
  prediction_id?: number
}