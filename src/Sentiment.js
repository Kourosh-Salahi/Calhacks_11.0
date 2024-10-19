import React from "react";
import PropTypes from "prop-types";
import { Box, Typography, Paper } from "@mui/material";

const Sentiment = ({ title = "Hello" }) => {
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
          height: "200px", // Simulate chatbox height
          overflowY: "auto", // Scrollable content if necessary
        }}
      >
        {/* This could be where the chat messages go */}
        <Typography variant="body1" color="textSecondary">
          Chat messages will appear here.
        </Typography>
      </Box>
    </Paper>
  );
};

Sentiment.propTypes = {
  title: PropTypes.string,
};

export default Sentiment;
