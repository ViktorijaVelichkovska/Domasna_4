import React, { useEffect, useState } from "react";
//import './LandingPageTable.css'

const LandingPageTable = () => {
    const [data, setData] = useState([]);
    const [message, setMessage] = useState("Please select a company.");
    const [selectedView, setSelectedView] = useState("risers"); // State to track selected view
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
                        avg_price: entry.avg_price || 0,
                        percentage: entry.percentage || "0.00",
                        best_price: entry.total_profit || 0,
                    }))
                );
            } catch (error) {
                console.error("Error fetching data:", error);
                setMessage("Error fetching data. Please try again.");
            }
        };
        fetchData();
    }, []);

    const risers = data.filter(
        (row) => parseFloat(row.percentage.replace(',', '.')) > 0
    );
    const fallers = data.filter(
        (row) => parseFloat(row.percentage.replace(',', '.')) < 0
    );
    const neutrals = data.filter(
        (row) => parseFloat(row.percentage.replace(',', '.')) === 0
    );

    // Function to handle changing view
    const handleViewChange = (view) => {
        setSelectedView(view);
    };

    return (
        <div className="table-container">
            <div className="table-1">
                <h1>Последно на маркетот</h1>
                {data.length === 0 ? (
                    <p>{message}</p>
                ) : (
                    <table className="market-table">
                        <thead>
                        <tr>
                            <th>Индекс</th>
                            <th>Просечна цена</th>
                            <th>% пром.</th>
                            <th>БЕСТ цена</th>
                        </tr>
                        </thead>
                        <tbody>
                        {data.map((row, index) => (
                            <tr key={index}>
                                <td>
                                    {/* Arrows on the left side */}
                                    <span className={`indicator ${
                                        parseFloat(row.percentage.replace(",", ".")) > 0 ? "up" :
                                            parseFloat(row.percentage.replace(",", ".")) < 0 ? "down" : "neutral"
                                    }`}>
                                            {parseFloat(row.percentage.replace(",", ".")) > 0 && (
                                                <span className="arrow up">↑</span>
                                            )}
                                        {parseFloat(row.percentage.replace(",", ".")) < 0 && (
                                            <span className="arrow down">↓</span>
                                        )}
                                        {parseFloat(row.percentage.replace(",", ".")) === 0 && (
                                            <span className="arrow neutral">•</span>
                                        )}
                                        {row.company_code}
                                        </span>
                                </td>
                                <td>{row.avg_price?.toLocaleString("mk-MK")}</td>
                                <td>{row.percentage}</td>
                                <td>{row.best_price?.toLocaleString("mk-MK")}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                )}
            </div>

            {/* Risers and Fallers Table with Toggle */}
            <div className="table-2">
                <h1>МБИ10</h1>
                <div className="view-toggle">
                    <button
                        className={selectedView === "risers" ? "active" : ""}
                        onClick={() => handleViewChange("risers")}
                    >
                        Risers
                    </button>
                    <button
                        className={selectedView === "fallers" ? "active" : ""}
                        onClick={() => handleViewChange("fallers")}
                    >
                        Fallers
                    </button>
                </div>

                <table className="risers-fallers-table">
                    <thead>
                    <tr>
                        <th>Индекс</th>
                        <th>Просечна цена</th>
                        <th>% пром.</th>
                        <th>БЕСТ цена</th>
                    </tr>
                    </thead>
                    <tbody>
                    {(selectedView === "risers" ? risers : fallers).map((row, index) => (
                        <tr key={index}>
                            <td>
                                {/* Arrows on the left side */}
                                <span className={selectedView === "risers" ? "up" : "down"}>
                                        {parseFloat(row.percentage.replace(",", ".")) > 0 && (
                                            <span className="arrow up">↑</span>
                                        )}
                                    {parseFloat(row.percentage.replace(",", ".")) < 0 && (
                                        <span className="arrow down">↓</span>
                                    )}
                                    {parseFloat(row.percentage.replace(",", ".")) === 0 && (
                                        <span className="arrow neutral">•</span>
                                    )}
                                    {row.company_code}
                                    </span>
                            </td>
                            <td>{row.avg_price?.toLocaleString("mk-MK")}</td>
                            <td>{row.percentage}</td>
                            <td>{row.best_price?.toLocaleString("mk-MK")}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default LandingPageTable;