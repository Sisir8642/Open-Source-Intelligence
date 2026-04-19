export type EntityType = 'company' | 'individual'
export type RiskLevel = 'high' | 'medium' | 'low' | 'unknown'
export type SearchStatus = 'pending' | 'running' | 'completed' | 'failed'
export type Category = 'social' | 'technical' | 'regulatory'
export type ReportFormat = 'markdown' | 'pdf'

export interface Finding {
  id: string
  adapter: string
  category: Category
  title: string
  description: string | null
  source_url: string | null
  raw_data: Record<string, unknown> | null
  confidence: number
  risk_level: RiskLevel
  is_mock: boolean
  fetched_at: string
}

export interface Search {
  id: string
  query: string
  entity_type: EntityType
  status: SearchStatus
  risk_level: RiskLevel
  risk_score: number
  confidence_score: number
  summary: string | null
  created_at: string
  completed_at: string | null
  findings: Finding[]
}

export interface SearchSummary {
  id: string
  query: string
  entity_type: EntityType
  status: SearchStatus
  risk_level: RiskLevel
  risk_score: number
  created_at: string
  finding_count: number
}

export interface Report {
  id: string
  search_id: string
  format: ReportFormat
  content: string | null
  created_at: string
}

export interface SearchRequest {
  query: string
  entity_type: EntityType
}

export interface ReportRequest {
  format: ReportFormat
}
