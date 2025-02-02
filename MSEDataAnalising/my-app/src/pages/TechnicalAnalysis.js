import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DataDisplay = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Извршување на GET барање кога компонентата се учита
        axios.get('http://127.0.0.1:8000/api/get_data/', {
            params: {
                company_code: '123',  // Пример за податоци кои можеш да ги пратиш
                start_date: '2024-01-01',
                end_date: '2024-01-31'
            }
        })
            .then((response) => {
                setData(response.data);  // Податоците се поставуваат во state
                setLoading(false);        // Завршена е задачата за вчитување
            })
            .catch((error) => {
                console.error('There was an error!', error);
                setLoading(false);
            });
    }, []); // Празниот низa [] значи дека ова ќе се изврши само еднаш

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Data from Backend</h1>
            <ul>
                {data.map((item, index) => (
                    <li key={index}>{item.company_name} - {item.date}</li>
                ))}
            </ul>
        </div>
    );
};

export default DataDisplay;
