import React from "react";
import PropTypes from "prop-types";
import { Box, Typography, Paper } from "@mui/material";
import { height } from "@mui/system";

const LandmarkFeed = ({ title = "Hello" }) => {
  return (
    <Paper
      elevation={3} // Adds a shadow for a more elevated look
      sx={{
        padding: "20px",
        backgroundColor: "#f5f5f5", // Light background color
        borderRadius: "16px", // Rounded corners
        width: "100%",
        maxWidth: "500px", // Limit width for chatbox
        margin: "20px auto", // Center horizontally and add top/bottom margin
        textAlign: "center", // Center text horizontally
        height: "100%", // Simulate chatbox height
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
          backgroundColor: "#ffffff", // Chat input area background
        }}
      >
        {/* This could be where the chat messages go */}
        <img src="http://localhost:5000/video_feed" alt="Camera Feed" />
      </Box>
    </Paper>
  );
};

LandmarkFeed.propTypes = {
  title: PropTypes.string,
};

export default LandmarkFeed;
