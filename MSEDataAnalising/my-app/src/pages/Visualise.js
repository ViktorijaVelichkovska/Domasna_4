import TimeSeriesGraph from "../components/VisualizationPage/TimeSeriesChart";
//import TimeSeriesContainer from "../components/TimeSeriesContainer";
import React from "react";
import VisualizeBackground from "../components/VisualizationPage/VisualizeBackground";
import './Visualise.css'
import TimeSeriesContainer from "../components/VisualizationPage/TimeSeriesContainer";
import AboutBackground from "../components/AboutPage/AboutBackground";
import Footer from "../components/Footer";

export default function Visualise() {
    return (
        <div id="vis-container">
            <VisualizeBackground/>
            <div id="vis-above">
                <h1>Визуелизација на податоци</h1>
            </div>
            <div id="vis-bellow"
                 style={{display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
                <h1>Графички приказ на податоци за издавачи</h1>
                <TimeSeriesContainer/>
            </div>
            <Footer/>
        </div>
    )


}