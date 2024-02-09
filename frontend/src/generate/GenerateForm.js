import React, {useEffect, useState} from 'react';
import './GenerateForm.css';
import Select from 'react-select';
import FileSaver from 'file-saver';


const API_BASE_URL = 'http://localhost:5000';

function Generate() {
    const [email, setEmail] = useState("Anonim");
    const [filename, setFilename] = useState("cardio_train.csv")
    const [error, setError] = useState(null);

    const [files, setFiles] = useState([])
    const [rows, setRows] = useState(100);

    const [newCsv, setNewCsv] = useState(null);

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

    fetch(`${API_BASE_URL}/files`, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
             credentials: 'include',
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
        .then(data => {
            setFiles(data["files"]);
        });

    const handleStartGenerate = (event) => {
        const data = {
            "filename": "cardio_train.csv",
            "rows": rows
        };
        const config = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        fetch(`${API_BASE_URL}/generate`, config)
            .then(response => response.blob())
            .then(blob => setNewCsv(blob))
            .catch(error => {
                console.error(error);
            });
    };

    function downloadFile() {
        const csvData = new Blob([newCsv], {type: 'text/csv;charset=utf-8;'});

        FileSaver.saveAs(csvData, 'data.csv')
    }

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
            <div className="file-select">
                <p>Выберите файл</p>
                <Select id="file-select"
                        options={files.map(t => ({label: t, value: t}))}
                        onChange={([selected]) => {
                            setFilename(selected)
                        }}
                >
                </Select>
            </div>
            <div className="generate-parameters">
                <div className="rows">
                    <p>Количество строк</p>
                    <input
                        type="text"
                        value={rows}
                        onChange={(e) => setRows(e.target.value)}
                    />
                </div>
            </div>
            <div className="buttons">
                <div className="start-generate">
                    <button type="button" onClick={handleStartGenerate}>Начать генерацию датасета</button>
                </div>

                {newCsv !== null ? <div className="download">
                    <button type="button" onClick={downloadFile}>Скачать</button>
                </div> : null}
            </div>
        </div>
    );
}

export default Generate;

function goToProfile() {
    window.location.href = '/profile';
}

function goToTrain() {
    window.location.href = '/train';
}

function goToGenerate() {
    window.location.href = '/generate';
}