import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import ShowData from './pages/ShowData';
import TechnicalAnalysis from './pages/TechnicalAnalysis';
import Navigation from './components/Navigation';

import Visualise from "./pages/Visualise";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Nlp_predictions from "./pages/nlp_predictions";




function App() {
    return (
        <Router>
            <div>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/show-data" element={<ShowData />} />
                    <Route path="/visualisation" element={<Visualise />} />
                    <Route path="/news" element={<Nlp_predictions />} />
                    <Route path="/technical-analysis" element={<TechnicalAnalysis />} />
                </Routes>
            </div>
        </Router>
    );
}





export default App;
