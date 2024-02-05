import React, {useEffect, useState} from 'react';
import './RootForm.css';
import CSVDataTable from "./CSVDataTable";


const API_BASE_URL = 'http://localhost:5000';

function Root() {
    const [csvData, setCsvData] = useState([]);
    const [email, setEmail] = useState("Anonim");
    const [filename, setFilename] = useState("cardio_train.csv")
    const [error, setError] = useState(null);

    const [numerical, setNumerical] = useState([]);
    const [selectedNumerical, setSelectedNumerical] = useState([]);

    const [categorical, setCategorical] = useState([]);
    const [selectedCategorical, setSelectedCategorical] = useState([]);
    const [isOpen, setIsOpen] = useState(false);


    const handleFileChange = async (event) => {
            const file = event.target.files[0];
            setFilename("file.name")

            const formData = new FormData();
            formData.append('file', file);

            const config = {
                method: 'POST',
                body: formData,
                contentType: 'Multipart/form-data'
            };

            const response = await fetch(`${API_BASE_URL}/upload`, config);
            if (response.status === 200) {
                fetch(`${API_BASE_URL}/properties/${filename}`, {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    }
                }).then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                    .then(data => {
                        setNumerical(data["numerical"]);
                        setCategorical(data["categorical"]);
                    });
            }

            if (file) {
                const reader = new FileReader();

                reader.onload = (e) => {
                    const csvText = e.target.result;
                    parseCSV(csvText);
                };

                reader.readAsText(file);
            }
        }
    ;

    const parseCSV = (csvText) => {
        const lines = csvText.split("\n");
        const headers = lines[0].split(",");
        const parsedData = [];

        for (let i = 1; i < lines.length; i++) {
            const currentLine = lines[i].split(",");

            if (currentLine.length === headers.length) {
                const row = {};
                for (let j = 0; j < headers.length; j++) {
                    row[headers[j].trim()] = currentLine[j].trim();
                }
                parsedData.push(row);
            }
        }

        setCsvData(parsedData);
    };

    useEffect(() => {
        fetch(`${API_BASE_URL}/profile`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
            }, credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setEmail(data["email"]);
            })
            .catch(error => {
                setEmail("Username");
            });
    }, []);

    const handleSelectChange = (event) => {
        setSelectedNumerical(current => [...current, event.target.value]);
    };

    function NumberDiv({number}) {
        return (
            <div
                style={{
                    backgroundColor: 'red',
                    padding: '5px',
                    margin: '5px',
                    borderRadius: '3px',
                    width: 'fit-content',
                    color: 'white'

                }}
            >
                {number}
            </div>
        );
    }

    const handleClick = () => {
        setIsOpen(!isOpen);
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="page">
            <div className="header">
                <div className="navigation">
                    <div className="train-generator">
                        <p>Обучить генератор</p>
                    </div>
                    <div className="generate-dataset">
                        <p>Сгенерировать датасет</p>
                    </div>
                </div>
                <div className="user-info">
                    <div className="username" onClick={() => goToProfile()}>
                        <p className="request-content">{email}</p>
                    </div>
                </div>
            </div>
            <div className="csv-container">
                <div className="upload-form">
                    <div className="upload-text">
                        <p> Загрузите ваш датасет</p>
                    </div>
                    <div className="upload-button">
                        <form>
                            <label htmlFor="upload-csv">Выбрать файл </label>
                            <input type="file" id="upload-csv" onChange={handleFileChange} accept=".csv"/>
                        </form>
                    </div>
                </div>
                <div className="csv-table">
                    <CSVDataTable data={csvData}/>
                </div>
            </div>
            <div className="properties-container">
                <div className="columns">
                    <div className="numerical">
                        <p onClick={handleClick} >Выберите числовые колонки</p>
                        <label htmlFor="numerical"></label>
                        {isOpen &&
                        <select id="numerical" multiple={true} value={selectedNumerical}
                                onChange={handleSelectChange}>
                            {numerical.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                        }

                        <div className="numericalItems">
                            {selectedNumerical.map((number, index) => (
                                <NumberDiv number={number} key={index}/>
                            ))}
                        </div>
                    </div>
                    <div className="categorical">
                        <p>Выберите категориальные колонки</p>
                        <label htmlFor="categorical"></label>
                        <select id="categorical" value={selectedCategorical}
                                onChange={(e) => setSelectedCategorical(e.target.value)}>
                            <option value=""></option>
                            {categorical.map((option, index) => (
                                <option key={index} value={option}>{option}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Root;

function goToProfile() {
    window.location.href = '/profile';
}