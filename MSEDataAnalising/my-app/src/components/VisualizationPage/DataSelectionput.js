import React from "react";

const DataSelectionInput = ({ companyCodes, selectedCompanyCode, startDate, endDate, onInputChange }) => {
    return (
        <div className="data-selection">
            <span>
                <label htmlFor="companyCode">Избери компанија: </label>
                <select
                    id="companyCode"
                    value={selectedCompanyCode}
                    onChange={(e) => onInputChange("selectedCompanyCode", e.target.value)}
                >
                    <option value="">--Избери компанија--</option>
                    {companyCodes.map((company, index) => (
                        <option key={index} value={company.code}>
                            {company.name}
                        </option>
                    ))}
                </select>
            </span>

            <span>
                <label htmlFor="startDate">Дата од: </label>
                <input
                    type="date"
                    id="startDate"
                    value={startDate}
                    onChange={(e) => onInputChange("startDate", e.target.value)}
                />
            </span>

            <span>
                <label htmlFor="endDate">Дата до: </label>
                <input
                    type="date"
                    id="endDate"
                    value={endDate}
                    onChange={(e) => onInputChange("endDate", e.target.value)}
                />
            </span>
        </div>
    );
};

export default DataSelectionInput;