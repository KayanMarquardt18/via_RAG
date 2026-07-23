import { BrowserRouter, Routes, Route } from "react-router-dom";

import BlackHole from "./components/BlackHole";
import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Predictor from "./pages/Predictor";
import Knowledge from "./pages/Knowledge";
import About from "./pages/About";

import "./styles/app.css";

function App() {
  return (
    <BrowserRouter>
      <BlackHole />
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/predictor" element={<Predictor />} />
        <Route path="/knowledge" element={<Knowledge />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;