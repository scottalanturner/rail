'use client'

import { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Actual UP Baird Subdivision coordinates through Aledo
const RAILROAD_PATH = [
  [32.701069, -97.635797],
  [32.700978, -97.634220],
  [32.700879, -97.631688],
  [32.700789, -97.629478],
  [32.700621, -97.626774],
  [32.700397, -97.624049],
  [32.700087, -97.621431],
  [32.699751, -97.618899],
  [32.699367, -97.616367],
  [32.698923, -97.613878],
  [32.698450, -97.611346],
  [32.697977, -97.608857],
  [32.697472, -97.606368],
  [32.696936, -97.603836],
  [32.696400, -97.601347],
  [32.695896, -97.598944],
  [32.695391, -97.596498],
  [32.694855, -97.593966],
  [32.694351, -97.591563],
  [32.693877, -97.589203]
];

const mapStyle = {
  height: '500px',
  width: '100%',
  position: 'relative' as const,
  zIndex: 0
}

// Custom train icon
const trainIcon = new L.Icon({
  iconUrl: '/train-icon.png',
  iconSize: [32, 32],
  iconAnchor: [16, 16],
  popupAnchor: [0, -16]
});

interface TrainPosition {
  lat: number
  lng: number
  direction: 'east' | 'west'
  timestamp: string
}

function interpolatePosition(start: number[], end: number[], fraction: number): [number, number] {
  return [
    start[0] + (end[0] - start[0]) * fraction,
    start[1] + (end[1] - start[1]) * fraction
  ];
}

export default function TrainMap() {
  const [mounted, setMounted] = useState(false)
  const [trainPosition, setTrainPosition] = useState<TrainPosition>({
    lat: RAILROAD_PATH[0][0],
    lng: RAILROAD_PATH[0][1],
    direction: 'east',
    timestamp: new Date().toISOString()
  })
  
  const animationRef = useRef<number>()
  const progressRef = useRef(0)
  const segmentRef = useRef(0)

  useEffect(() => {
    let startTime: number

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp
      const progress = (timestamp - startTime) / 60000 // Complete journey in 60 seconds

      progressRef.current = progress % 1
      const totalProgress = progress % 2 // 2 for round trip

      const isEastbound = totalProgress < 1
      const direction = isEastbound ? 'east' : 'west'
      
      const pathLength = RAILROAD_PATH.length - 1
      let segmentProgress: number
      
      if (isEastbound) {
        segmentProgress = totalProgress * pathLength
        segmentRef.current = Math.floor(segmentProgress)
      } else {
        segmentProgress = (2 - totalProgress) * pathLength
        segmentRef.current = Math.floor(segmentProgress)
      }

      const segmentIndex = Math.min(segmentRef.current, pathLength - 1)
      const start = isEastbound ? 
        RAILROAD_PATH[segmentIndex] : 
        RAILROAD_PATH[pathLength - segmentIndex]
      const end = isEastbound ? 
        RAILROAD_PATH[segmentIndex + 1] : 
        RAILROAD_PATH[pathLength - segmentIndex - 1]

      const segmentFraction = segmentProgress % 1
      const [lat, lng] = interpolatePosition(start, end, segmentFraction)

      setTrainPosition({
        lat,
        lng,
        direction,
        timestamp: new Date().toISOString()
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animationRef.current = requestAnimationFrame(animate)

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [])

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div style={mapStyle} className="bg-gray-100 flex items-center justify-center">
        Loading map...
      </div>
    )
  }

  return (
    <div style={mapStyle}>
      <MapContainer
        center={[32.698450, -97.611346]} // Center of Aledo
        zoom={14}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        <Polyline 
          positions={RAILROAD_PATH}
          color="black"
          weight={3}
        />

        <Marker
          position={[trainPosition.lat, trainPosition.lng]}
          icon={trainIcon}
        />
      </MapContainer>
    </div>
  )
}