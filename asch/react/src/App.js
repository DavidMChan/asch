import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
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
  return (<CookiesProvider>
    <Router>
      <Switch>
        <Route exact path="/" component={Index} />
        <Route path="/play" component={PlayView} />
        <Route path="/login" component={LoginView} />
        <PrivateRoute path="/results" component={ResultsView} />
      </Switch>
    </Router>

    <ToastContainer />
  </CookiesProvider>)
}
