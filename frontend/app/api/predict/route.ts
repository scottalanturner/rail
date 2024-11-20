import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  
  try {
    // Here you would call your backend API/Lambda function
    // This is a placeholder response
    const prediction = {
      probability: Math.random(), // Replace with actual prediction
      timeWindow: `${body.time} - ${body.day}`,
    }
    
    return NextResponse.json(prediction)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get prediction' },
      { status: 500 }
    )
  }
} 