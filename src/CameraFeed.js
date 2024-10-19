"use client";

import React, { useState, useEffect, useRef } from "react";
import PropTypes from "prop-types";
import {
  Button,
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
} from "@mui/material";

const CameraFeed = ({ title = "Camera Feed" }) => {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    return () => {
      // Cleanup: stop the stream when component unmounts
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      streamRef.current = stream;
      setIsCameraActive(true);
      setError(null);
    } catch (err) {
      console.error("Error accessing the camera:", err);
      setError(
        "Failed to access the camera. Please make sure you have given permission and your camera is working."
      );
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
  };

  const toggleCamera = () => {
    if (isCameraActive) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  return (
    <Card sx={{ maxWidth: 400, margin: "0 auto", boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" component="div" align="center" gutterBottom>
          {title}
        </Typography>

        <Box
          sx={{
            position: "relative",
            paddingBottom: "56.25%",
            backgroundColor: "#f0f0f0",
            borderRadius: 1,
          }}
        >
          <video ref={videoRef} autoPlay playsInline muted style={videoStyle} />
        </Box>

        {error && (
          <Typography color="error" sx={{ marginTop: 2 }}>
            {error}
          </Typography>
        )}
      </CardContent>

      <CardActions>
        <Button
          fullWidth
          variant="contained"
          color={isCameraActive ? "error" : "primary"}
          onClick={toggleCamera}
        >
          {isCameraActive ? "Stop Camera" : "Start Camera"}
        </Button>
      </CardActions>
    </Card>
  );
};

// PropTypes validation
CameraFeed.propTypes = {
  title: PropTypes.string,
};

// Basic inline styles for the video element
const videoStyle = {
  position: "absolute",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  objectFit: "cover",
};

export default CameraFeed;
