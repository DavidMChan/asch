import React from 'react';
import Unity, { UnityContext } from 'react-unity-webgl';
import { toast } from 'react-toastify';
import { build_request } from '../utils';
import queryString from 'query-string';
import Cookies from 'js-cookie'


export default class ResultsView extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            participants: null,
            experiment: null,
        };

        this.download = this.download.bind(this);
    }

    download() {
        const url = this.state.experiment === null ? '/api/v0/data/download' : `/api/v0/data/download?experiment=${this.state.experiment}`;
        fetch(url, {method: 'GET', headers: {
            'x-access-tokens': Cookies.get('session')
        }}).then((resp) => {
            if (resp.status != 200) {
                toast.error('Unable to download experiment data.', {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            } else {
                resp.blob().then((blob) => {
                    var file = window.URL.createObjectURL(blob);
                    window.location.assign(file);
                  });
            }
        });
    }

    componentDidMount() {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if ('experiment' in urlParams) {
            this.setState({experiment: urlParams.get('experiment')})
        }
    }


    render() {
            return (<div className="h-screen w-screen grid justify-items-center">
                        <div className="m-auto">
                        <button className="m-3 p-3 text-base font-semibold rounded-full block border-2 border-purple-300 hover:bg-purple-300 text-purple-700"
                                type="button"
                                onClick={this.download}>Download All Results</button>
                        </div>
                    </div>);
    }

}
