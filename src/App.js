import React from "react";
import CameraFeed from "./CameraFeed";
import LiveChatBox from "./LiveChatBox";
import { Box } from "@mui/material";
import Sentiment from "./Sentiment";
import LiveVideoAnalysis from "./All";
import LandmarkFeed from "./LandmarkFeed";

function App() {
  return (
    <>
      {/* Live Video Analysis could be used here */}
      <Box
        display="flex"
        flexDirection="row" 
        justifyContent="space-between" 
        alignItems="flex-start" 
        padding="20px"
        gap="20px" 
        width="100%" 
      >
        <Box flex="1" maxWidth="50%">
          {/* First Box for CameraFeed */}
          <CameraFeed title="Live Feed" />
        </Box>

        <Box flex="1" maxWidth="50%">
          {/* Second Box for LandmarkFeed */}
          <LandmarkFeed title="Landmark Detection" />
        </Box>
      </Box>

      <Box
        display="flex"
        flexDirection="row" 
        justifyContent="space-between" 
        alignItems="flex-start" 
        padding="20px"
        gap="20px" 
        width="100%" 
      >
        <Box flex="1" maxWidth="50%">
          {/* First Box for Sentiment */}
          <Sentiment title="Sentiment Analysis:" />
        </Box>

        <Box flex="1" maxWidth="50%">
          {/* Second Box for LiveChatBox */}
          <LiveChatBox title="Welcome to the Live Chat!" />
        </Box>
      </Box>
    </>
  );
}

export default App;
