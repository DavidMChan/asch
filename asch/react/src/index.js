import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import './tailwind.output.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { Windmill } from '@windmill/react-ui'


ReactDOM.render(
  <React.StrictMode>
    <Windmill>
      <App />
    </Windmill>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
