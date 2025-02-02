import React, { useEffect, useState } from 'react';
import Papa from 'papaparse';
import { Link } from 'react-router-dom';

const ShowData = () => {
    const [companies, setCompanies] = useState([]); // Листа на компании
    const [selectedCompany, setSelectedCompany] = useState(null); // Избрана компанија
    const [companyData, setCompanyData] = useState([]); // Податоци за избраната компанија


    useEffect(() => {
        fetch('/csv/files.json')
            .then((response) => response.json())
            .then((data) => {
                setCompanies(data);
            })
            .catch((error) => {
                console.error('Грешка при вчитување на companies:', error);
            });
    }, []);


    const loadCompanyData = (companyFile) => {
        fetch(`/csv/${companyFile}`)
            .then((response) => response.text())
            .then((csvText) => {
                Papa.parse(csvText, {
                    header: true,
                    complete: (results) => {
                        const last10YearsData = results.data.filter((row) => {
                            const year = new Date(row.date).getFullYear();
                            return year >= new Date().getFullYear() - 10;
                        });
                        setCompanyData(last10YearsData);
                    },
                    error: (error) => {
                        console.error('Грешка при парсирање на CSV:', error);
                    },
                });
            })
            .catch((error) => {
                console.error('Грешка при вчитување на CSV:', error);
            });
    };

    return (
        <div style={{ backgroundColor: '#001f3f', color: '#FFD700', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            {/* Header */}
            <header style={headerStyle}>
                <img
                    src="logo.jpg"
                    alt="Лого на Македонска берза"
                    style={{ height: '60px', marginRight: '20px' }}
                />
                <nav style={navStyle}>
                    <Link to="/" style={linkStyle}>Home</Link>
                    <Link to="/show-data" style={linkStyle}>Show Data</Link>
                    <Link to="/about" style={linkStyle}>About</Link>
                </nav>
            </header>

            {/* Main Content */}
            <main style={mainContentStyle}>
                <h1 style={{ fontSize: '3em', textShadow: '2px 2px 5px rgba(0, 0, 0, 0.7)' }}>Изберете компанија од берзата</h1>


                {companies.length > 0 ? (
                    <div>
                        {companies.map((company, index) => (
                            <button
                                key={index}
                                onClick={() => loadCompanyData(company)}
                                style={{
                                    margin: '10px',
                                    padding: '10px 20px',
                                    backgroundColor: '#B8860B',
                                    color: 'white',
                                    border: 'none',
                                    cursor: 'pointer',
                                    fontSize: '1.1em',
                                    fontWeight: 'bold',
                                    transition: 'background-color 0.3s',
                                }}
                            >
                                {company.replace('.csv', '')}
                            </button>
                        ))}
                    </div>
                ) : (
                    <p>Не се најдени компании.</p>
                )}


                {companyData.length > 0 && (
                    <div>
                        <h2>Податоци за {selectedCompany}</h2>
                        <table
                            style={{
                                margin: '0 auto',
                                borderCollapse: 'collapse',
                                width: '80%',
                                textAlign: 'left',
                            }}
                        >
                            <thead>
                            <tr>
                                {Object.keys(companyData[0]).map((key) => (
                                    <th
                                        key={key}
                                        style={{
                                            border: '1px solid #ddd',
                                            padding: '8px',
                                            backgroundColor: '#FFA500',
                                            color: 'white',
                                            textTransform: 'uppercase',
                                            fontSize: '14px',
                                        }}
                                    >
                                        {key}
                                    </th>
                                ))}
                            </tr>
                            </thead>
                            <tbody>
                            {companyData.map((row, index) => (
                                <tr key={index}>
                                    {Object.values(row).map((value, i) => (
                                        <td key={i} style={{ border: '1px solid #ddd', padding: '8px' }}>
                                            {value}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer style={footerStyle}>
                <p>© 2024 Македонска берза. Сите права се задржани.</p>
            </footer>
        </div>
    );
};

export default ShowData;

// Styles (Reusing the same styles as in Home page)
const headerStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#001f3f',
    padding: '10px 20px',
    borderBottom: '2px solid #FFD700',
    color: '#FFD700',
};

const navStyle = {
    display: 'flex',
    gap: '15px',
};

const linkStyle = {
    color: '#FFD700',
    textDecoration: 'none',
    fontSize: '1.1em',
    fontWeight: 'bold',
    transition: 'color 0.3s',
};

linkStyle[':hover'] = {
    color: '#FFA500',
};

const mainContentStyle = {
    flex: 1,
    textAlign: 'center',
    padding: '50px 20px',
};

const footerStyle = {
    textAlign: 'center',
    padding: '15px 0',
    backgroundColor: '#001f3f',
    color: '#FFD700',
    borderTop: '2px solid #FFD700',
};
