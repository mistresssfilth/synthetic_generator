import React, {Fragment} from "react";
import { BrowserRouter as Router, Navigate, Routes, Route, Link } from "react-router-dom";

import LoginForm from './login/LoginForm';
import RegistrationForm from './registration/RegistrationForm';

import {handleLogin} from './login/LoginForm';
import {handleRegistration} from './registration/RegistrationForm';

import Profile from "./profile/Profile";
import Root from "./root/RootForm";

function App() {
    return (
        <div className="App">
            <Router>
                <Fragment>
                    <Routes>
                        <Route exact path="/" element={<Root/>}/>
                        <Route exact path="/login" element={<LoginForm onLogin={handleLogin}/>}/>
                        <Route exact path="/registration"
                               element={<RegistrationForm onRegistration={handleRegistration}/>}
                        />
                        <Route exact path="/profile" element={<Profile/>}/>
                        <Route path="*" element={<Navigate to="/" replace/>}/>
                    </Routes>
                </Fragment>
            </Router>
        </div>
    );
}

export default App;