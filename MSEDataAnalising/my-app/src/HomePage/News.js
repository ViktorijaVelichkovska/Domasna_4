import React, { useEffect, useState } from "react";
//import "./News.css";

export default function News() {
    const [data, setData] = useState([]);
    const [selectedNews, setSelectedNews] = useState(null);

    useEffect(() => {
        const fetchCompanyPredictions = async () => {
            try {
                const response = await fetch(
                    `http://localhost:8000/nlp/api/get-latest-newss/`
                );
                const data = await response.json();
                setData(data.slice(0, 3)); // Only get the first 3 latest news
            } catch (error) {
                console.error("Error fetching company predictions:", error);
            }
        };
        fetchCompanyPredictions();
    }, []);

    const truncateContent = (content) => {
        if (!content) return "Опис на новоста";
        const maxLength = 200; // Show more content
        return content.length > maxLength ? content.substring(0, maxLength) + "..." : content;
    };

    const openModal = (news) => {
        setSelectedNews(news);
    };

    const closeModal = () => {
        setSelectedNews(null);
    };

    return (
        <div id="news">
            <h2>Последно на маркетот</h2>
            <p className="p">Биди во тек со последните актуелни новости на полето на Македонската берза</p>
            {data.length > 0 ? (
                <div className="news-cards">
                    {data.map((entry, index) => (
                        <div
                            className="news-card"
                            key={index}
                            onClick={() => openModal(entry)}
                        >
                            <h3>{entry.company_name || "Наслов"}</h3>
                            <p>{truncateContent(entry.content)}</p>
                            <p><strong>Датум:</strong> {entry.date || "N/A"}</p>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="no-data">No data available.</div>
            )}

            {selectedNews && (
                <div className="modal-overlay" onClick={closeModal}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h3>{selectedNews.company_name || "Наслов"}</h3>
                        <p>{selectedNews.content || "Опис на новоста"}</p>
                        <p><strong>Датум:</strong> {selectedNews.date || "N/A"}</p>
                        <button onClick={closeModal}>Затвори</button>
                    </div>
                </div>
            )}
        </div>
    );
}