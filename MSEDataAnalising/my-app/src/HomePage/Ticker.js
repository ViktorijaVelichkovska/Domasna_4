import React, { useEffect, useState } from 'react';
//import './Ticker.css';

const Ticker = () => {
    const [data, setData] = useState([]);
    const [message, setMessage] = useState("Loading data...");
    const selectedCompanyCode = "ALK,GRNT,KMB,MPT,REPL,SBT,STB,TEL,TTK";

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(
                    `http://localhost:8000/api/get-last-day-data/?company_codes=${selectedCompanyCode}`
                );
                const responseData = await response.json();
                setData(
                    responseData.map((entry) => ({
                        company_code: entry.company_code || "N/A",
                        last_transaction_price: entry.last_transaction_price || 0,
                        percentage: entry.percentage || "0.00"
                    }))
                );
            } catch (error) {
                console.error("Error fetching data:", error);
                setMessage("Error fetching data. Please try again.");
            }
        };

        fetchData();
    }, []);

    return (
        <div className="ticker-wrapper">
            {data.length === 0 ? (
                <p>{message}</p>
            ) : (
                <div className="ticker-content">
                    {data.map((item, index) => (
                        <div key={index} className="ticker-item">
                            <div className="company-code">{item.company_code}</div>
                            <div className="transaction-details">
                                <span className="transaction-price">
                                    {item.last_transaction_price.toLocaleString('mk-MK')}
                                </span>
                                <span
                                    className={`percentage ${
                                        parseFloat(item.percentage.replace(',', '.')) > 0
                                            ? 'up'
                                            : parseFloat(item.percentage.replace(',', '.')) < 0
                                                ? 'down'
                                                : 'neutral' // Handle 0% change (no movement)
                                    }`}
                                >
                                    {item.percentage}%
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Ticker;