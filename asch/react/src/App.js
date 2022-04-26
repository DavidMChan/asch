import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CookiesProvider } from 'react-cookie';
import { ToastContainer } from 'react-toastify';

import PrivateRoute from './components/private_route';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';

// Core navigational pages
import Index from './views/index';
import PlayView from './views/play';
import ResultsView from './views/results';
import LoginView from './views/login';

export default function App() {
    return (
        <CookiesProvider>
            <Router>
                <Routes>
                    <Route exact path="/" element={<Index />} />
                    <Route path="/play" element={<PlayView />} />
                    <Route path="/login" element={<LoginView />} />
                    <Route
                        path="/results"
                        element={
                            <PrivateRoute>
                                <ResultsView />
                            </PrivateRoute>
                        }
                    />
                </Routes>
            </Router>

            <ToastContainer />
        </CookiesProvider>
    );
}
