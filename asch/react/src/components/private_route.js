// This is used to determine if a user is authenticated and
// if they are allowed to visit the page they navigated to.

// If they are: they proceed to the page
// If not: they are redirected to the login page.
import React from 'react';
import { Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';

function PrivateRoute({ children }) {
    var isLoggedIn = false;
    if (Cookies.get('session') !== null) {
        const path = window.location.protocol + '//' + window.location.host + '/api/v0/validate_session';
        var request = new XMLHttpRequest();
        request.open('GET', path, false); // `false` makes the request synchronous
        request.setRequestHeader('Authorization', Cookies.get('session'));
        request.send(null);
        if ('error' in JSON.parse(request.response)) {
            Cookies.remove('session');
        } else {
            isLoggedIn = true;
        }
    }

    return isLoggedIn ? children : <Navigate to="/login" />;
}

// const PrivateRoute = ({ component: Component, ...rest }) => {
//     return (
//         <Route
//             {...rest}
//             render={(props) =>
//                 isLoggedIn ? (
//                     <Component {...props} />
//                 ) : (
//                     <Route path="/" element={<Navigate to="/login" />} />
//                     // <Route
//                     //     path="login"
//                     //     render={() => <Redirect to={{ pathname: '/login', state: { from: props.location } }} />}
//                     // />
//                     // <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
//                 )
//             }
//         />
//     );
// };

export default PrivateRoute;
