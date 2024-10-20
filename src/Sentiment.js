import React, { useState, useEffect } from 'react';
import PropTypes from "prop-types";
import { Box, Typography, Paper } from "@mui/material";

const Sentiment = ({ title = "Hello" }) => {
  const [sentiment, setSentiment] = useState('Loading...'); // Default is 'Loading...'

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://localhost:5000/sentiment')
        .then(response => response.json())
        .then(data => {
          setSentiment(data.sentiment); // Update with the sentiment from the API
        })
        .catch(error => console.error('Error fetching sentiment status:', error));
    }, 1000); // Poll every 1 second

    return () => clearInterval(interval);
  }, []);

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
        <Typography variant="h3" color="textSecondary">
          {sentiment} {/* Display the sentiment fetched from the API */}
        </Typography>
      </Box>
    </Paper>
  );
};

Sentiment.propTypes = {
  title: PropTypes.string,
};

export default Sentiment;
