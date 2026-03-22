import { ArrowUpRight, ArrowDownRight } from 'lucide-react'

interface RegionalData {
  state: string
  enrolment_impact: number
  update_impact: number
  total_impact: number
}

interface RegionalImpactTableProps {
  regionalData: RegionalData[]
}

export default function RegionalImpactTable({ regionalData }: RegionalImpactTableProps) {
  const formatNumber = (num: number) => {
    return num.toLocaleString()
  }

  const getImpactLevel = (impact: number, maxImpact: number) => {
    const percentage = (impact / maxImpact) * 100
    if (percentage >= 80) return { level: 'Very High', color: 'text-red-600 bg-red-50' }
    if (percentage >= 60) return { level: 'High', color: 'text-orange-600 bg-orange-50' }
    if (percentage >= 40) return { level: 'Medium', color: 'text-yellow-600 bg-yellow-50' }
    if (percentage >= 20) return { level: 'Low', color: 'text-blue-600 bg-blue-50' }
    return { level: 'Very Low', color: 'text-gray-600 bg-gray-50' }
  }

  const maxImpact = Math.max(...regionalData.map(d => d.total_impact))

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">
          Regional Impact Analysis
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          Top 10 states by expected policy impact
        </p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rank
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                State
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Total Impact
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Enrollment Impact
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Update Impact
              </th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Impact Level
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {regionalData.map((row, index) => {
              const impactLevel = getImpactLevel(row.total_impact, maxImpact)
              return (
                <tr key={row.state} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className="text-sm font-medium text-gray-900">
                        #{index + 1}
                      </span>
                      {index < 3 && (
                        <ArrowUpRight className="ml-1 h-4 w-4 text-red-500" />
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {row.state}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <div className="text-sm font-semibold text-gray-900">
                      {formatNumber(row.total_impact)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <div className="text-sm text-green-600">
                      {formatNumber(row.enrolment_impact)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <div className="text-sm text-purple-600">
                      {formatNumber(row.update_impact)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-center">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${impactLevel.color}`}>
                      {impactLevel.level}
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div>
            Showing top {regionalData.length} states by impact volume
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span>Enrollment Impact</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-purple-500 rounded-full mr-2"></div>
              <span>Update Impact</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}