import React, {useEffect, useState} from 'react';
import './Profile.css';

const API_BASE_URL = 'http://localhost:5000';


function Profile() {
    const [username, setUsername] = useState(
        {
            "email": 'Нет электронной почты'
        }
    );

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
                setUsername(data);
            });
    }, []);


    const logout = () => {
        fetch(`${API_BASE_URL}/logout`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
            }, credentials: 'include',
        })
            .then(() => {
                goToLogin()
            })
    };

    return (
        <div className="me-container">
            <div className="avatar">
                <p>🐈</p>
            </div>
            <header className="username-header">
                {username.username}
            </header>
            <div className="username-content">
                <p>{username.email}</p>
                {username.departments !== "" ? (
                    <p>{username.departments}</p>
                ) : (
                    <p>Не состоит в отделах</p>
                )}
            </div>
            <button className="logout" onClick={() => logout()}>Завершить сеанс</button>
        </div>);
}

function goToLogin() {
    window.location.href = '/login';
}

export default Profile;