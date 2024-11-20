'use client'

import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { Icon } from 'leaflet'

// Aledo coordinates
const ALEDO_CENTER = [32.6960, -97.6022]
const RAILROAD_PATH = [
  [32.6965, -97.6122], // Adjust these coordinates to match actual railroad
  [32.6960, -97.6022],
  [32.6955, -97.5922]
]

// Custom train icon
const trainIcon = new Icon({
  iconUrl: '/train-icon.png', // You'll need to add this image to public folder
  iconSize: [32, 32]
})

interface TrainPosition {
  lat: number
  lng: number
  direction: 'east' | 'west'
  timestamp: string
}

export default function TrainMap() {
  const [trainPosition, setTrainPosition] = useState<TrainPosition | null>(null)

  useEffect(() => {
    // Set up WebSocket connection
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL!)
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'train_position') {
        setTrainPosition(data.position)
      }
    }

    return () => ws.close()
  }, [])

  return (
    <div className="h-[500px] w-full">
      <MapContainer
        center={ALEDO_CENTER}
        zoom={14}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {/* Railroad track line */}
        <Polyline 
          positions={RAILROAD_PATH}
          color="black"
          weight={3}
        />

        {/* Train marker */}
        {trainPosition && (
          <Marker
            position={[trainPosition.lat, trainPosition.lng]}
            icon={trainIcon}
          />
        )}
      </MapContainer>
    </div>
  )
} 