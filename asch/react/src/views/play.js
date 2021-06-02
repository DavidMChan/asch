


import React from 'react';
import Unity, { UnityContext } from 'react-unity-webgl';
import { toast } from 'react-toastify';
import { build_request } from '../utils';
import queryString from 'query-string';

/*
participant:
    experiment:
        build_path: str
    id: str
    mturk:
        completion_code: str
*/


function LoadingScreen(props) {
    return (<div className="h-screen w-screen grid justify-items-center">
                <div className="m-auto">Game is loading. Please wait.</div>
            </div>);
}

function ErrorScreen(props) {
    return (<div className="h-screen w-screen grid justify-items-center">
                <div className="m-auto">
                    <div className="text-center text-red-600">Error fetching data from server.</div>
                    <div className="text-center">Please verify the link you used to visit this site and try again.</div>
                </div>
            </div>);
}

function CompletionScreen(props) {
    return (<div className="h-screen w-screen grid justify-items-center">
                <div className="m-auto text-3xl">Finished. Completion code: {props.mturk_code}</div>

            </div>);
}

function GameScreen(props) {
    return (<div className="h-screen w-screen grid justify-items-center">
                <div className="game m-auto" id="gameWindow">
                    <Unity unityContext={props.unityContext} className="h-100 w-100"/>
                    <div>Note: This may take some time to load depending on your internet and computer speed. Thank you for your patience.</div>
                </div>
            </div>);
}



export default class PlayView extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            participant: null,
            is_loading: true,
            is_finished: false,
            is_error: false,
        }
    }

    componentDidMount() {

        // Parse the query string for information on the game
        let params = queryString.parse(this.props.location.search);
        var request = null;
        if ('pid' in params) {
            request = build_request(`/api/v0/play?pid=${params.pid}`);
        } else if ('experiment' in params) {
            if ('condition' in params) {
                request = build_request(`/api/v0/play?experiment=${params.experiment}&condition=${params.condition}`);
            } else {
                request = build_request(`/api/v0/play?experiment=${params.experiment}`);
            }
        } else {
            toast.error('Must pass experiment, condition or play ID when visiting this endpoint.', {
                position: 'top-right',
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
            });
            this.setState({
                is_loading: false,
                is_error: true,
            })
        }


        // Fetch the participant data from the server
        const that = this; // Handle pinning of function in async captures.
        fetch(request).then((response) => {
            if (response.status !== 200) {
                toast.error('Error fetching data from server. Try refreshing the page, or checking the link for correctness.', {
                    position: 'top-right',
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
                that.setState({
                    is_loading: false,
                    is_error: true,
                })
            }

            response.json().then((participant) => {
                // Load the unity game
                that.unityContent = new UnityContext({
                    loaderUrl: `../static/games/${participant.experiment.build_path}/Build/unity.loader.js`,
                    dataUrl: `../static/games/${participant.experiment.build_path}/Build/unity.data`,
                    frameworkUrl: `../static/games/${participant.experiment.build_path}/Build/unity.framework.js`,
                    codeUrl: `../static/games/${participant.experiment.build_path}/Build/unity.wasm`,
                });

                // Send the participant data to the unity game
                const host = window.location.protocol + "//" + window.location.host;
                that.unityContent.on('ReadyToReceiveData', () => {
                    that.unityContent.send('ParticipantSettings', 'SetParticipantId', participant.id);
                    that.unityContent.send('ParticipantSettings', 'SetServerUrl', host);
                });

                // Set up the exit hooks
                // TODO: that needs to be adjusted so it won't show the completion code if the participant isn't actually done.
                that.unityContent.on('quitted', () => {
                    console.log('Game state: Finished.');
                    that.setState({ is_finished: true, is_loading: false, is_error: false});
                });

                // Finish the loading process
                that.setState({
                    participant: participant,
                    is_loading: false});
            }).catch((e) => {
                toast.error('Error fetching data from server. Try refreshing the page, or checking the link for correctness.', {
                    position: 'top-right',
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
                that.setState({
                    is_loading: false,
                    is_error: true,
                })
            });
        });
    }

    render() {
        if (this.state.is_loading) {
            return <LoadingScreen />;
        } else if (this.state.is_error) {
            return <ErrorScreen />;
        } else if (this.state.is_finished || this.state.participant && this.state.participant._finished) {
            return <CompletionScreen mturk_code={this.state.participant.mturk_data.completion_code}/>;
        } else {
            return <GameScreen unityContext={this.unityContent}/>
        }
    }

}
