import React from 'react';
import Unity, { UnityContext } from 'react-unity-webgl';
import { toast } from 'react-toastify';
import { build_request } from '../utils';
import queryString from 'query-string';
import { faDownload, faTrash } from '@fortawesome/free-solid-svg-icons';
import Cookies from 'js-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

class ParticipantCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            participant: props.participant,
            onDelete: props.onDelete,
            onDownload: props.onDownload,
        };
    }

    render() {
        return (
            <div className="px-2">
                <div className="bg-white px-4 pt-3 flex my-2 rounded-lg shadow">
                    <div className="flex-1">
                        <p>
                            <b>Name:</b> {this.state.participant.name}
                        </p>
                        <p>
                            <b>Condition:</b> {this.state.participant.condition}
                        </p>
                        <p>
                            <b>MTURK Code:</b> {this.state.participant.mturk_data.completion_code}
                        </p>
                        <p>
                            <b>Last Seen:</b> {this.state.participant._last_seen}
                        </p>
                        <p style={{ textAlign: 'right' }}>
                            <a href="#" onClick={() => this.state.onDownload(this.state.participant)}>
                                <FontAwesomeIcon icon={faDownload} className="px-2" />
                            </a>
                            <a href="#" onClick={() => this.state.onDelete(this.state.participant)}>
                                <FontAwesomeIcon icon={faTrash} className="px-2" />
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        );
    }
}

export default class ResultsView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            participants: null,
            experiment: null,
        };

        this.download = this.download.bind(this);
        this.onDelete = this.onDelete.bind(this);
        this.onDownload = this.onDownload.bind(this);
    }

    download() {
        const url =
            this.state.experiment === null
                ? '/api/v0/data/download'
                : `/api/v0/data/download?experiment=${this.state.experiment}`;
        fetch(url, {
            method: 'GET',
            headers: {
                'x-access-tokens': Cookies.get('session'),
            },
        }).then((resp) => {
            if (resp.status != 200) {
                toast.error('Unable to download experiment data.', {
                    position: 'top-right',
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

    onDelete(participant) {
        const url = `/api/v0/participants?id=${participant._id}`;
        fetch(url, {
            method: 'DELETE',
            headers: {
                'x-access-tokens': Cookies.get('session'),
            },
        }).then((resp) => {
            if (resp.status != 200) {
                toast.error('Unable to delete participant.', {
                    position: 'top-right',
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            } else {
                toast.success('Participant deleted.', {
                    position: 'top-right',
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
                this.setState({ participants: this.state.participants.filter((p) => p._id != participant._id) });
            }
            // window.location.reload(false);
        });
    }

    onDownload(participant) {
        const url =
            this.state.experiment === null
                ? '/api/v0/data/download?id=' + participant._id
                : `/api/v0/data/download?experiment=${this.state.experiment}&id=${participant._id}`;
        fetch(url, {
            method: 'GET',
            headers: {
                'x-access-tokens': Cookies.get('session'),
            },
        }).then((resp) => {
            if (resp.status != 200) {
                toast.error('Unable to download participant data.', {
                    position: 'top-right',
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
            this.setState({ experiment: urlParams.get('experiment') });
        }

        const url =
            urlParams.get('experiment') === null
                ? '/api/v0/participants'
                : `/api/v0/participants?experiment=${urlParams.get('experiment')}`;
        const that = this;
        fetch(url, { method: 'GET', headers: { 'x-access-tokens': Cookies.get('session') } }).then((resp) => {
            if (resp.status != 200) {
                toast.error('Unable to fetch participant data.', {
                    position: 'top-right',
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            } else {
                resp.json().then((data) => {
                    that.setState({ participants: data, experiment: urlParams.get('experiment') });
                });
            }
        });
    }

    render() {
        return (
            <div className="h-screen w-screen grid justify-items-center">
                <div className="m-auto w-100">
                    <div className="my-20">
                        <h1 className="text-3xl text-center">
                            {this.state.experiment === null
                                ? 'Experimental Results'
                                : 'Experimental Results: ' + this.state.experiment}
                        </h1>
                    </div>
                    <button
                        className="p-2 my-4 text-base font-semibold rounded-full block border-2 border-purple-300 hover:bg-purple-300 text-purple-700"
                        type="button"
                        onClick={this.download}
                        style={{ margin: '0 auto', display: 'block' }}>
                        Download All Results
                    </button>

                    {this.state.participants === null || this.state.participants.length === 0 ? (
                        <React.Fragment />
                    ) : (
                        <div className="w-4/5 flex mx-auto">
                            <div className="p-6 border rounded-t-lg bg-gray-100">
                                <div className="flex flex-wrap -mx-2 items-center justify-center">
                                    {this.state.participants.map((p) => (
                                        <ParticipantCard
                                            participant={p}
                                            key={p._id}
                                            onDelete={this.onDelete}
                                            onDownload={this.onDownload}
                                        />
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}
