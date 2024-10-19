'use client'

import React, { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

const CameraFeed = ({ title = "Camera Feed" }) => {
  const [isCameraActive, setIsCameraActive] = useState(false)
  const [error, setError] = useState(null)
  const videoRef = useRef(null)
  const streamRef = useRef(null)

  useEffect(() => {
    return () => {
      // Cleanup: stop the stream when component unmounts
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }
      streamRef.current = stream
      setIsCameraActive(true)
      setError(null)
    } catch (err) {
      console.error('Error accessing the camera:', err)
      setError('Failed to access the camera. Please make sure you have given permission and your camera is working.')
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
    setIsCameraActive(false)
  }

  const toggleCamera = () => {
    if (isCameraActive) {
      stopCamera()
    } else {
      startCamera()
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="aspect-video bg-muted rounded-md overflow-hidden">
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            muted 
            className="w-full h-full object-cover"
          />
        </div>
        {error && (
          <p className="text-destructive mt-2">{error}</p>
        )}
      </CardContent>
      <CardFooter>
        <Button onClick={toggleCamera} className="w-full">
          {isCameraActive ? 'Stop Camera' : 'Start Camera'}
        </Button>
      </CardFooter>
    </Card>
  )
}

CameraFeed.propTypes = {
  title: PropTypes.string
}

export default CameraFeed