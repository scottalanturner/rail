import dynamic from 'next/dynamic'
import TrainPredictionForm from '@/components/TrainPredictionForm'

// Disable SSR for the map component since it needs browser APIs
const TrainMap = dynamic(() => import('@/components/TrainMap'), { 
  ssr: false 
})

export default function Home() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">
        Aledo Train Monitor
      </h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-md p-4">
          <h2 className="text-xl font-semibold mb-4">Live Train Map</h2>
          <TrainMap />
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <h2 className="text-xl font-semibold mb-4">Train Predictions</h2>
          <TrainPredictionForm />
        </div>
      </div>
    </div>
  )
} 