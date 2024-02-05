import React, {useEffect, useState} from 'react';
import '../registration/RegistrationForm.css';
import {registerUser} from "../api";

const API_BASE_URL = 'http://localhost:5000';

function RegistrationForm({onRegistration}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        onRegistration(email, password, setErrorMessage);
    };

    return (
        <div className="login-form-container">
            <header className="login-header">
                Регистрация
            </header>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <form className="login-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="email">Электронная почта</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Пароль</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Зарегистрироваться</button>
                <button onClick={() => goToLogin()} className="hint">Вход</button>
            </form>
        </div>);
}

export async function handleRegistration(email, password, setErrorMessage) {
    try {
        const response = await registerUser({email, password});

        if (response === 200) {
            localStorage.setItem('authToken', response.token);

            window.location.href = '/login';
            console.error('Registration was successful, token provided in the response.');
        } else {
            console.error('Registration was unsuccessful, no token provided in the response.');
            setErrorMessage('Невозможно зарегистрировать пользователя с данным логином/почтой');
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
        setErrorMessage('Невозможно зарегистрировать пользователя с данным логином/почтой');
    }
}

function goToLogin() {
    window.location.href = '/login';
}

export default RegistrationForm;