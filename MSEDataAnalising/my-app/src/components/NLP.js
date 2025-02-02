import React, {useEffect, useState} from "react";

export default function NLP() {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchCompanyPredictions = async () => {
            try {
                const response = await fetch(
                    `http://localhost:8000/nlp/api/get-company-predictions/`);
                const data = await response.json();
                setData(data);
            } catch (error) {
                console.error("Error fetching company predictions:", error);
            }
        };
        fetchCompanyPredictions();
    }, []);


    return (
        <div className="data-table">
            <table border="1">
                <thead>
                <tr>
                    <th>Company code</th>
                    <th>Company name</th>
                    <th>Prediction</th>
                </tr>
                </thead>
                <tbody>
                {data.length > 0 ? (
                    data.map((entry, index) => (
                        <tr key={index}>
                            <td>{entry.company_code || "N/A"}</td>
                            <td>{entry.company_name || "N/A"}</td>
                            <td>{entry.max_sentiment || "N/A"}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="2" style={{textAlign: "center"}}>
                            No data available.
                        </td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
}