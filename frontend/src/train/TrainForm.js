import React, {useEffect, useState} from 'react';
import './TrainForm.css';
import CSVDataTable from "./CSVDataTable";
import Select from 'react-select';

const API_BASE_URL = 'http://localhost:5000';

function Train() {
    const [csvData, setCsvData] = useState([]);
    const [email, setEmail] = useState("Anonim");
    const [filename, setFilename] = useState("cardio_train.csv")
    const [error, setError] = useState(null);

    const [numerical, setNumerical] = useState([]);
    const [selectedNumerical, setSelectedNumerical] = useState([]);

    const [categorical, setCategorical] = useState([]);
    const [selectedCategorical, setSelectedCategorical] = useState([]);

    const [batchSize, setBatchSize] = useState(500);
    const [learningRate, setLearningRate] = useState(0.05);
    const [epochs, setEpochs] = useState(100);

    const handleFileChange = async (event) => {
            const file = event.target.files[0];
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

    const handleStartTraining = (event) => {
        const data = {
            "filename": "cardio_train.csv",
            "numerical": selectedNumerical,
            "categorical": selectedCategorical,
            "batchSize": batchSize,
            "learningRate": learningRate,
            "epochs": epochs
        };
        const config = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        fetch(`${API_BASE_URL}/train`, config)
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.error(error);
            });
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="page">
            <div className="header">
                <div className="navigation">
                    <div className="train-generator" onClick={() => goToTrain()}>
                        <p>Обучить генератор</p>
                    </div>
                    <div className="generate-dataset" onClick={() => goToGenerate()}>
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
                        <p>Выберите числовые колонки</p>
                        <Select id="numerical"
                                isMulti
                                options={numerical.map(t => ({label: t, value: t}))}
                                onChange={([selected]) => {
                                    setSelectedNumerical(selected)
                                }}
                        >
                        </Select>
                    </div>
                    <div className="categorical">
                        <p>Выберите категориальные колонки</p>
                        <Select id="categorical"
                                isMulti
                                options={categorical.map(t => ({label: t, value: t}))}
                                onChange={([selected]) => {
                                    setSelectedCategorical(selected)
                                }}
                        >
                        </Select>
                    </div>
                </div>
                <div className="model-parameters">
                    <p>Выберите параметры модели</p>
                    <div className="model-parameters-container">
                        <div className="batch-size">
                            <p>Batch size</p>
                            <input
                                type="text"
                                value={batchSize}
                                onChange={(e) => setBatchSize(e.target.value)}
                            />
                        </div>
                        <div className="learning-rate">
                            <p>Learning rate</p>
                            <input
                                type="text"
                                value={learningRate}
                                onChange={(e) => setLearningRate(e.target.value)}
                            />
                        </div>
                    </div>
                </div>
                <div className="training-parameters">
                    <div className="epochs">
                        <p>Epochs</p>
                        <input
                            type="text"
                            value={epochs}
                            onChange={(e) => setEpochs(e.target.value)}
                        />
                    </div>
                </div>
            </div>
            <div className="start-training">
                {csvData.length > 0 ?
                    <button type="button" onClick={handleStartTraining}>Запустить обучение</button>
                    : <p>Для обучения модели необходимо загрузить csv файл.</p>}
            </div>
        </div>
    );
}

export default Train;

function goToProfile() {
    window.location.href = '/profile';
}

function goToTrain() {
    window.location.href = '/train';
}

function goToGenerate() {
    window.location.href = '/generate';
}