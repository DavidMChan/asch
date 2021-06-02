import React from 'react';
import Unity, { UnityContext } from 'react-unity-webgl';
import { toast } from 'react-toastify';
import { build_request } from '../utils';
import queryString from 'query-string';
import Cookies from 'js-cookie';
import { Redirect } from 'react-router';


export default class LoginView extends React.Component {

    constructor(props) {

        super(props);

        this.state = {
            username: '',
            password: '',
            logged_in: false,
        };

        this.login = this.login.bind(this);
        this.onPasswordChange = this.onPasswordChange.bind(this);
        this.onUsernameChange = this.onUsernameChange.bind(this);
        this.handleKeyDown = this.handleKeyDown.bind(this);
    }

    login(event) {
        event.preventDefault();
        const that = this;
        fetch('/api/v0/login', {
            method: 'POST',
            headers: {
                'Authorization': btoa(this.state.username + ':' + this.state.password),
            }
        }).then((resp) => resp.json().then((data) => {
            if ('error' in data) {
                toast.error('Invalid Username / Password', {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            } else {
                Cookies.set('session', data.token, { expires: 1 });
                this.setState({logged_in: true});
            }
        }));
    }

    onPasswordChange(event) {
        this.setState({ password: event.target.value });
    }

    onUsernameChange(event) {
        this.setState({ username: event.target.value });
    }

    handleKeyDown(event) {
        if (event.key === 'Enter') {
            this.login(event);
        }
    }

    componentDidMount() {
        if (Cookies.get('session') !== null) {
            const path = window.location.protocol + '//' + window.location.host + '/api/v0/validate_session';
            var request = new XMLHttpRequest();
            request.open('GET', path, false);
            request.setRequestHeader('Authorization', Cookies.get('session'));
            request.send(null);
            if ('error' in JSON.parse(request.response)) {
                Cookies.remove('session')
            } else {
                this.setState({logged_in: true});
            }
        }
    }

    render() {

            if (this.state.logged_in) {
                return <Redirect to='/' />
            }

            return (<div className="h-screen w-screen grid justify-items-center">
                        <div className="m-auto">
                            <div className="w-full max-w-xs">
                                <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                                    <div className="mb-4">
                                        <label className="block text-gray-700 text-sm font-bold mb-2">
                                            Username
                                        </label>
                                        <input
                                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                            id="username"
                                            type="text"
                                            placeholder="Username"
                                            onChange={this.onUsernameChange} />
                                    </div>
                                    <div className="mb-6">
                                        <label className="block text-gray-700 text-sm font-bold mb-2">
                                            Password
                                        </label>
                                        <input
                                            className="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                                            id="password"
                                            type="password"
                                            placeholder="******************"
                                            onChange={this.onPasswordChange}
                                            onKeyDown={this.handleKeyDown}/>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <button
                                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                                            type="button"
                                            onClick={this.login}>
                                            Sign In
                                        </button>
                                    </div>
                                </form>
                                <p className="text-center text-gray-500 text-xs">
                                    &copy; 2021 UC Berkeley. All rights reserved.
                                </p>
                            </div>
                        </div>
                    </div>);
    }

}
