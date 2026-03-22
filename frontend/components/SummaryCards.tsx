import { Users, TrendingUp, Calendar, BarChart3 } from 'lucide-react'

interface SummaryData {
  total_people_affected: number
  total_enrolment_impact: number
  total_update_impact: number
  average_daily_impact: number
  policy_date: string
  forecast_days: number
}

interface SummaryCardsProps {
  summary: SummaryData
}

export default function SummaryCards({ summary }: SummaryCardsProps) {
  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toLocaleString()
  }

  const cards = [
    {
      title: 'Total People Affected',
      value: formatNumber(summary.total_people_affected),
      rawValue: summary.total_people_affected.toLocaleString(),
      icon: Users,
      color: 'blue',
      description: 'Expected total impact across all states'
    },
    {
      title: 'Enrollment Impact',
      value: formatNumber(summary.total_enrolment_impact),
      rawValue: summary.total_enrolment_impact.toLocaleString(),
      icon: TrendingUp,
      color: 'green',
      description: 'New enrollments expected'
    },
    {
      title: 'Update Impact',
      value: formatNumber(summary.total_update_impact),
      rawValue: summary.total_update_impact.toLocaleString(),
      icon: BarChart3,
      color: 'purple',
      description: 'Updates expected (bio + demo)'
    },
    {
      title: 'Daily Average',
      value: formatNumber(summary.average_daily_impact),
      rawValue: summary.average_daily_impact.toLocaleString(),
      icon: Calendar,
      color: 'orange',
      description: 'Average daily impact volume'
    }
  ]

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-50 text-blue-600 border-blue-200',
      green: 'bg-green-50 text-green-600 border-green-200',
      purple: 'bg-purple-50 text-purple-600 border-purple-200',
      orange: 'bg-orange-50 text-orange-600 border-orange-200'
    }
    return colors[color as keyof typeof colors] || colors.blue
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const Icon = card.icon
        return (
          <div
            key={card.title}
            className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow animate-slide-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600 mb-1">
                  {card.title}
                </p>
                <p className="text-2xl font-bold text-gray-900 mb-1">
                  {card.value}
                </p>
                <p className="text-xs text-gray-500">
                  {card.rawValue} total
                </p>
              </div>
              <div className={`p-3 rounded-lg border ${getColorClasses(card.color)}`}>
                <Icon className="h-6 w-6" />
              </div>
            </div>
            <div className="mt-4">
              <p className="text-xs text-gray-500">
                {card.description}
              </p>
            </div>
          </div>
        )
      })}
    </div>
  )
}