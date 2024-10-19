import React, { useState, useRef, useEffect } from "react";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Typography,
  TextField,
} from "@mui/material";

export default function LiveVideoAnalysis() {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isVideoActive, setIsVideoActive] = useState(false);
  const cameraRef = useRef(null);
  const videoRef = useRef(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (cameraRef.current) {
        cameraRef.current.srcObject = stream;
        setIsCameraActive(true);
      }
    } catch (err) {
      console.error("Error accessing the camera:", err);
    }
  };

  const stopCamera = () => {
    if (cameraRef.current && cameraRef.current.srcObject) {
      const tracks = cameraRef.current.srcObject.getTracks();
      tracks.forEach((track) => track.stop());
      setIsCameraActive(false);
    }
  };

  useEffect(() => {
    return () => {
      stopCamera(); // Cleanup when component unmounts
    };
  }, []);

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(to bottom right, #1f2937, #1c1f26)",
        padding: "32px",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "auto",
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "32px",
        }}
      >
        {/* Live Camera Feed */}
        <Card
          style={{
            background: "linear-gradient(to bottom right, #1c1f26, #2a2e37)",
          }}
        >
          <div style={{ padding: "16px" }}>
            {" "}
            {/* Using a basic div instead of CardHeader for debugging */}
            <Typography variant="h5" style={{ color: "#ffffff" }}>
              Live Camera Feed
            </Typography>
          </div>
          <CardContent>
            <div
              style={{
                position: "relative",
                paddingBottom: "56.25%",
                background: "#000",
                borderRadius: "8px",
                overflow: "hidden",
              }}
            >
              <video
                ref={cameraRef}
                autoPlay
                playsInline
                muted
                style={{
                  width: "100%",
                  height: "100%",
                  position: "absolute",
                  top: 0,
                  left: 0,
                  objectFit: "cover",
                }}
              />
            </div>
            <Button
              onClick={isCameraActive ? stopCamera : startCamera}
              variant="contained"
              color="primary"
              fullWidth
              style={{
                marginTop: "16px",
                background: "linear-gradient(to right, #42a5f5, #1e88e5)",
              }}
            >
              {isCameraActive ? "Stop Camera" : "Start Camera"}
            </Button>
          </CardContent>
        </Card>

        {/* Video Input */}
        <Card
          style={{
            background: "linear-gradient(to bottom right, #1c1f26, #2a2e37)",
          }}
        >
          <div style={{ padding: "16px" }}>
            <Typography variant="h5" style={{ color: "#ffffff" }}>
              Video Input
            </Typography>
          </div>
          <CardContent>
            <div
              style={{
                position: "relative",
                paddingBottom: "56.25%",
                background: "#000",
                borderRadius: "8px",
                overflow: "hidden",
              }}
            >
              <video
                ref={videoRef}
                controls
                style={{
                  width: "100%",
                  height: "100%",
                  position: "absolute",
                  top: 0,
                  left: 0,
                  objectFit: "cover",
                }}
              >
                <source src="/placeholder.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
            <TextField
              type="file"
              accept="video/*"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file && videoRef.current) {
                  videoRef.current.src = URL.createObjectURL(file);
                  setIsVideoActive(true);
                }
              }}
              fullWidth
              style={{ marginTop: "16px" }}
            />
          </CardContent>
        </Card>

        {/* Sentiment Analysis */}
        <Card
          style={{
            background: "linear-gradient(to bottom right, #1c1f26, #2a2e37)",
          }}
        >
          <div style={{ padding: "16px" }}>
            <Typography variant="h5" style={{ color: "#ffffff" }}>
              Sentiment Analysis
            </Typography>
          </div>
          <CardContent>
            <div
              style={{
                height: "200px",
                backgroundColor: "#111827",
                borderRadius: "8px",
                padding: "16px",
                color: "#9CA3AF",
                overflowY: "auto",
              }}
            >
              Sentiment analysis results will appear here.
            </div>
          </CardContent>
        </Card>

        {/* Live Text Translation */}
        <Card
          style={{
            background: "linear-gradient(to bottom right, #1c1f26, #2a2e37)",
          }}
        >
          <div style={{ padding: "16px" }}>
            <Typography variant="h5" style={{ color: "#ffffff" }}>
              Live Text Translation
            </Typography>
          </div>
          <CardContent>
            <div
              style={{
                height: "200px",
                backgroundColor: "#111827",
                borderRadius: "8px",
                padding: "16px",
                color: "#9CA3AF",
                overflowY: "auto",
              }}
            >
              Live text translation will appear here.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
