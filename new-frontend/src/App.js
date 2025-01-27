import React, { useState } from "react";
import "./App.css";
import Weathercurrent from "./components/Weathercurrent";
import Weatherperiod from "./components/Weatherperiod";

function App() {
  
  return (
    <div>
<Weathercurrent />
{/* <Weathertable /> */}
<Weatherperiod />
      
    </div>
  );
}

export default App;
