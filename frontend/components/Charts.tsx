import { useEffect, useRef } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface DailyImpact {
  date: string
  enrolment_impact: number
  update_impact: number
  total_impact: number
}

interface RegionalImpact {
  top_10_states: Array<{
    state: string
    enrolment_impact: number
    update_impact: number
    total_impact: number
  }>
}

interface PeakAnalysis {
  peak_date: string
  peak_volume: number
  peak_enrolments: number
  peak_updates: number
}

interface ChartsProps {
  dailyImpact: DailyImpact[]
  regionalImpact: RegionalImpact
  peakAnalysis: PeakAnalysis
}

export default function Charts({ dailyImpact, regionalImpact, peakAnalysis }: ChartsProps) {
  // Daily Impact Line Chart
  const dailyChartData = {
    labels: dailyImpact.map(d => new Date(d.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Total Impact',
        data: dailyImpact.map(d => d.total_impact),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Enrollment Impact',
        data: dailyImpact.map(d => d.enrolment_impact),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        fill: false,
        tension: 0.4
      },
      {
        label: 'Update Impact',
        data: dailyImpact.map(d => d.update_impact),
        borderColor: 'rgb(168, 85, 247)',
        backgroundColor: 'rgba(168, 85, 247, 0.1)',
        fill: false,
        tension: 0.4
      }
    ]
  }

  const dailyChartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Daily Impact Forecast'
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            if (typeof value === 'number') {
              return value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value.toString()
            }
            return value
          }
        }
      }
    }
  }

  // Regional Impact Bar Chart
  const regionalChartData = {
    labels: regionalImpact.top_10_states.map(s => s.state),
    datasets: [
      {
        label: 'Enrollment Impact',
        data: regionalImpact.top_10_states.map(s => s.enrolment_impact),
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgb(34, 197, 94)',
        borderWidth: 1
      },
      {
        label: 'Update Impact',
        data: regionalImpact.top_10_states.map(s => s.update_impact),
        backgroundColor: 'rgba(168, 85, 247, 0.8)',
        borderColor: 'rgb(168, 85, 247)',
        borderWidth: 1
      }
    ]
  }

  const regionalChartOptions: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Top 10 States by Impact'
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 45
        }
      },
      y: {
        beginAtZero: true,
        stacked: true,
        ticks: {
          callback: function(value) {
            if (typeof value === 'number') {
              return value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value.toString()
            }
            return value
          }
        }
      }
    }
  }

  return (
    <div className="space-y-8">
      {/* Daily Impact Chart */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div className="h-80">
          <Line data={dailyChartData} options={dailyChartOptions} />
        </div>
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">Peak Impact Analysis</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-blue-700">Peak Date:</span>
              <span className="ml-2 font-medium">
                {new Date(peakAnalysis.peak_date).toLocaleDateString()}
              </span>
            </div>
            <div>
              <span className="text-blue-700">Peak Volume:</span>
              <span className="ml-2 font-medium">
                {peakAnalysis.peak_volume.toLocaleString()}
              </span>
            </div>
            <div>
              <span className="text-blue-700">Peak Breakdown:</span>
              <span className="ml-2 font-medium">
                {peakAnalysis.peak_enrolments.toLocaleString()} enrollments, {peakAnalysis.peak_updates.toLocaleString()} updates
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Regional Impact Chart */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div className="h-80">
          <Bar data={regionalChartData} options={regionalChartOptions} />
        </div>
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            This chart shows the top 10 states with the highest expected impact from the policy change.
            The stacked bars represent the breakdown between enrollment and update impacts.
          </p>
        </div>
      </div>
    </div>
  )
}