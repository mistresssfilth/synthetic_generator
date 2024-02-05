import React from "react";

const CSVDataTable = ({data}) => {
    const headers = data.length > 0 ? Object.keys(data[0]) : [];

    return (
        <>
            {data.length === 0 ? (
                <p>Данные не найдены.</p>
            ) : (
                <div>
                    <table style={tableScrollStyle}>
                        <thead>
                        <tr>
                            {headers.map((header, index) => (
                                <th key={index} style={tableHeaderStyle}>
                                    {header}
                                </th>
                            ))}
                        </tr>
                        </thead>
                    </table>
                    <div style={scrollBody}>
                        <table style={tableStyle}>
                            <tbody>
                            {data.map((row, index) => (
                                <tr key={index}>
                                    {headers.map((header, columnIndex) => (
                                        <td key={columnIndex} style={tableCellStyle}>
                                            {row[header]}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </>
    );
};

const scrollBody = {
    height: "450px",
    width: "calc(100vw - 600px)",
    overflow: "auto",
};

const tableStyle = {
    borderCollapse: "collapse",
    width: "100%",
    borderRadius: "10px",
    overflow: "hidden",
    boxShadow: "40px 90px 55px -20px rgba(155, 184, 243, 0.2)",
    tableLayout: "fixed",

};

const tableScrollStyle = {
    borderCollapse: "collapse",
    width: "calc(100vw - 600px)",
    borderRadius: "10px",
    overflow: "hidden",
    boxShadow: "40px 90px 55px -20px rgba(155, 184, 243, 0.2)",
    tableLayout: "fixed",

};

const tableHeaderStyle = {
    fontSize: "14px",
    fontWeight: 500,
    color: "#ffffff",
    backgroundColor: "#5D8AA8",
    borderBottom: "1px solid #ddd",
    padding: "15px",
    textAlign: "left",
};

const tableCellStyle = {
    fontSize: "14px",
    fontWeight: 500,
    borderBottom: "1px solid #ddd",
    padding: "15px",
    textAlign: "left",
    backgroundColor: "#fff",
};

export default CSVDataTable;