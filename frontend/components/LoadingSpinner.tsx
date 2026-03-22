export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        {/* Outer ring */}
        <div className="w-16 h-16 border-4 border-blue-200 rounded-full animate-spin"></div>
        {/* Inner ring */}
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-blue-600 rounded-full animate-spin"></div>
      </div>
      
      <div className="mt-6 text-center">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Generating Prediction
        </h3>
        <p className="text-gray-600 mb-4">
          Analyzing policy impact across all states...
        </p>
        
        {/* Progress steps */}
        <div className="space-y-2 text-sm text-gray-500">
          <div className="flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span>Loading historical data</span>
          </div>
          <div className="flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }}></div>
            <span>Running ML models</span>
          </div>
          <div className="flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
            <span>Calculating regional impact</span>
          </div>
          <div className="flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" style={{ animationDelay: '1.5s' }}></div>
            <span>Generating visualizations</span>
          </div>
        </div>
      </div>
      
      <div className="mt-6 text-xs text-gray-400 text-center">
        This usually takes 30-60 seconds
      </div>
    </div>
  )
}