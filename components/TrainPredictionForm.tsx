'use client'

import { useState } from 'react'

interface Prediction {
  probability: number
  timeWindow: string
}

export default function TrainPredictionForm() {
  const [selectedDay, setSelectedDay] = useState<string>('')
  const [selectedTime, setSelectedTime] = useState<string>('')
  const [prediction, setPrediction] = useState<Prediction | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          day: selectedDay,
          time: selectedTime,
        }),
      })
      
      const data = await response.json()
      setPrediction(data)
    } catch (error) {
      console.error('Failed to fetch prediction:', error)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Day of Week
          </label>
          <select
            value={selectedDay}
            onChange={(e) => setSelectedDay(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          >
            <option value="">Select a day</option>
            <option value="monday">Monday</option>
            <option value="tuesday">Tuesday</option>
            <option value="wednesday">Wednesday</option>
            <option value="thursday">Thursday</option>
            <option value="friday">Friday</option>
            <option value="saturday">Saturday</option>
            <option value="sunday">Sunday</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Time
          </label>
          <input
            type="time"
            value={selectedTime}
            onChange={(e) => setSelectedTime(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Get Prediction
        </button>
      </form>

      {prediction && (
        <div className="mt-6 p-4 bg-gray-100 rounded-md">
          <h3 className="text-lg font-medium text-gray-900">Prediction Result</h3>
          <p className="mt-2 text-gray-600">
            Time Window: {prediction.timeWindow}
          </p>
          <p className="text-gray-600">
            Probability: {(prediction.probability * 100).toFixed(1)}%
          </p>
        </div>
      )}
    </div>
  )
} 