import React from "react";
import CameraFeed from "./CameraFeed";
import LiveChatBox from "./LiveChatBox";
import { Box } from "@mui/material";
import Sentiment from "./Sentiment";
import LiveVideoAnalysis from "./All";

function App() {
  return (
    <LiveVideoAnalysis />
    // <>
    //   <Box
    //     display="flex"
    //     flexDirection="row" // Arrange items in a row (horizontally)
    //     justifyContent="space-between" // Space between the boxes
    //     alignItems="flex-start" // Align items at the top
    //     padding="20px"
    //     gap="20px" // Add gap between the boxes
    //     width="100%" // Ensure the container takes full width
    //   >
    //     <Box flex="1" maxWidth="50%">
    //       {" "}
    //       {/* First Box for CameraFeed */}
    //       <CameraFeed title="Live Feed" />
    //     </Box>

    //     <Box flex="1" maxWidth="50%">
    //       {" "}
    //       {/* Second Box for LiveChatBox */}
    //     </Box>
    //   </Box>
    //   <Box
    //     display="flex"
    //     flexDirection="row" // Arrange items in a row (horizontally)
    //     justifyContent="space-between" // Space between the boxes
    //     alignItems="flex-start" // Align items at the top
    //     padding="20px"
    //     gap="20px" // Add gap between the boxes
    //     width="100%" // Ensure the container takes full width
    //   >
    //     <Box flex="1" maxWidth="50%">
    //       {" "}
    //       {/* First Box for CameraFeed */}
    //       <Sentiment title="Sentiment Analysis:" />
    //     </Box>

    //     <Box flex="1" maxWidth="50%">
    //       {" "}
    //       {/* Second Box for LiveChatBox */}
    //       <LiveChatBox title="Welcome to the Live Chat!" />
    //     </Box>
    //   </Box>
    // </>
  );
}

export default App;
