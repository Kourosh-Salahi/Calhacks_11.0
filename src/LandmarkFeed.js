import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper } from '@mui/material';

const LandmarkFeed = ({ title = "Landmark Detection" }) => {
  const [inFrame, setInFrame] = useState(true); // Default is true (stable)

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://localhost:5000/inframe_status')
        .then(response => response.json())
        .then(data => {
          setInFrame(data.inframe);
        })
        .catch(error => console.error('Error fetching in-frame status:', error));
    }, 1000); // Poll every 1 second

    return () => clearInterval(interval);
  }, []);

  return (
    <Paper
      elevation={3}
      sx={{
        padding: "20px",
        backgroundColor: "#f5f5f5",
        borderRadius: "16px",
        width: "100%",
        maxWidth: "500px",
        margin: "20px auto",
        textAlign: "center",
        height: "100%",
      }}
    >
      <Typography variant="h5" component="div" gutterBottom>
        {title}
      </Typography>
      <Box
        sx={{
          padding: "10px",
          border: "2px solid #e0e0e0",
          borderRadius: "8px",
          backgroundColor: "#ffffff",
        }}
      >
        <img src="http://localhost:5000/video_feed" alt="Camera Feed" />
        <Box
          padding="20px"
          border="1px solid black"
          borderRadius="8px"
          backgroundColor={inFrame ? "#4CAF50" : "#FF5252"} // Green if stable, red if not
        >
          <Typography variant="h5">{title}</Typography>
          <Typography variant="body1">
            {inFrame ? "Stable" : "Please keep your hands and face in frame"}
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
};

export default LandmarkFeed;   
