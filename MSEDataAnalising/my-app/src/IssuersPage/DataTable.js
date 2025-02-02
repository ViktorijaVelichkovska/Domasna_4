import React, {useEffect, useState} from "react";
import './DataTable.css'

export default function DataTable() {
    const [data, setData] = useState([]);
    const [companyCodes, setCompanyCodes] = useState([]);
    const [selectedCompanyCode, setSelectedCompanyCode] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [message, setMessage] = useState("Молиме изберете компанија.");
    const [chartData, setChartData] = useState([]);

    // Fetch all company codes on component mount
    useEffect(() => {
        const fetchCompanyCodes = async () => {
            try {
                const response = await fetch("http://localhost:8000/api/get-company-codes/");
                const companyCodes = await response.json();
                setCompanyCodes(companyCodes);
            } catch (error) {
                console.error("Грешка при вчитување на кодови на компании:", error);
            }
        };

        fetchCompanyCodes();
    }, []);

    // Update the message based on the selected company and dates
    useEffect(() => {
        if (!selectedCompanyCode) {
            setMessage("Изберете компанија.");
        } else if (!startDate || !endDate) {
            setMessage("Изберете Датум од и Датум до.");
        } else {
            setMessage(""); // Clear the message when all required inputs are selected
        }
    }, [selectedCompanyCode, startDate, endDate]);

    // Fetch data when valid inputs are provided
    useEffect(() => {
        if (selectedCompanyCode && startDate && endDate) {
            const fetchData = async () => {
                try {
                    const response = await fetch(
                        `http://localhost:8000/api/get-data/?company_code=${selectedCompanyCode}&start_date=${startDate}&end_date=${endDate}`
                    );
                    const data = await response.json();
                    setData(data);

                    const formattedData = data.map((entry) => ({
                        timestamp: entry.date,
                        value: parseFloat(entry.total_profit.replace('.', '').replace(',', '.')),
                    }));

                    console.log("Форматирани податоци за график:", formattedData);
                    setChartData(formattedData);
                } catch (error) {
                    console.error("Грешка при вчитување на податоци:", error);
                    setMessage("Грешка при вчитување на податоци. Молиме обидете се повторно.");
                }
            };

            fetchData();
        }
    }, [selectedCompanyCode, startDate, endDate]);

    // Handle dropdown change
    const handleCompanyCodeChange = (event) => {
        setSelectedCompanyCode(event.target.value);
    };

    // Handle date change
    const handleStartDateChange = (event) => {
        setStartDate(event.target.value);
    };

    const handleEndDateChange = (event) => {
        setEndDate(event.target.value);
    };

    return (
        <div className="data-table">
            <div>
                <span>
                    {/* Dropdown menu for selecting a company */}
                    <label htmlFor="companyCode">Изберете компанија: </label>
                    <select
                        id="companyCode"
                        value={selectedCompanyCode}
                        onChange={handleCompanyCodeChange}
                    >
                        <option value="">--Изберете Компанија--</option>
                        {companyCodes.map((company, index) => (
                            <option key={index} value={company.code}>
                                {company.name}
                            </option>
                        ))}
                    </select>
                </span>

                <span>
                    {/* Date range pickers */}
                    <label htmlFor="startDate">Датум од: </label>
                    <input
                        type="date"
                        id="startDate"
                        value={startDate}
                        onChange={handleStartDateChange}
                    />
                </span>

                <span>
                    <label htmlFor="endDate">Датум до: </label>
                    <input
                        type="date"
                        id="endDate"
                        value={endDate}
                        onChange={handleEndDateChange}
                    />
                </span>
            </div>

            {/* Display message if necessary */}
            {message && <p style={{color: "red"}}>{message}</p>}

            <table border="1">
                <thead>
                <tr>
                    <th>Датум</th>
                    <th>Цена на последна трансакција</th>
                    <th>Макс.</th>
                    <th>Мин.</th>
                    <th>Просечна цена</th>
                    <th>% пром.</th>
                    <th>Количина</th>
                    <th>Промет во БЕСТ</th>
                    <th>Издавач</th>
                </tr>
                </thead>
                <tbody>
                {data.length > 0 ? (
                    data.map((entry, index) => (
                        <tr key={index}>
                            <td>{entry.date_string || "Н/А"}</td>
                            <td>{entry.last_transaction_price || "Н/А"}</td>
                            <td>{entry.max_price || "Н/А"}</td>
                            <td>{entry.min_price || "Н/А"}</td>
                            <td>{entry.avg_price || "Н/А"}</td>
                            <td>{entry.percentage || "Н/А"}</td>
                            <td>{entry.profit || "Н/А"}</td>
                            <td>{entry.total_profit || "Н/А"}</td>
                            <td>{entry.company_code || "Н/А"}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="9" style={{textAlign: "center"}}>
                            Нема податоци достапни.
                        </td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
}