import React from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
} from "recharts";
//import './TimeSeriesChart.css'; // Import the CSS file for styling

const TimeSeriesChart = ({ chartData }) => {
    const formatXAxis = (tick) => {
        const date = new Date(tick);
        return `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`;
    };

    const formatYAxis = (tick) => {
        return `${new Intl.NumberFormat('de-DE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(tick)} МКД`;
    };

    return (
        <div className="chart-container">
            {chartData.length > 0 ? (
                <LineChart
                    width={window.innerWidth * 0.6}
                    height={window.innerHeight* 0.6}
                    data={chartData}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        dataKey="timestamp"
                        tickFormatter={formatXAxis}
                        label={{ value: "Датум", position: "insideBottom", offset: 0 }}
                    />
                    <YAxis
                        tickFormatter={formatYAxis}
                        label={{ value: "Цена (МКД)", angle: -45, position: "insideLeft", offset: -20 }}
                    />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="value" stroke="#8884d8" />
                </LineChart>
            ) : (
                <p>Нема достапни податоци за избраните влезни параметри.</p>
            )}
        </div>
    );
};

export default TimeSeriesChart;