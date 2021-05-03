import React, { useState } from 'react';
import {
    Link
} from "react-router-dom";
import { Card, CardBody, Button, Backdrop } from '@windmill/react-ui'

function Launch(props) {
    return  <div className="flex items-center justify-center h-screen z-50 w-screen relative" onClick={props.onClick}>
                <div className="bg-indigo-800 text-white font-bold rounded-lg border shadow-lg p-10">
                    Centered Content
                </div>
            </div>;
}


function GameCard(props) {
    return (<Card className="flex h-48 border-2 border-gray-300 w-6/12 m-6">
                <img className="object-cover w-1/3" src="https://picsum.photos/800" />
                <CardBody>
                    <p className="mb-4 font-semibold text-gray-600 dark:text-gray-300">{props.name}</p>
                    <Button className="shadow-md mr-6" onClick={() => props.play_fn(props.name)}>Play</Button>
                    <Button className="shadow-md">View Results / Manage</Button>
                </CardBody>
            </Card>)
}


export default function Index() {

    const [playMode, setPlayMode] = useState(false);
    const [selectedGame, setSelectedGame ] = useState(null);

    function disable_play() {
        setPlayMode(false);
    }

    function play_fn(game) {
        setPlayMode(true);
        setSelectedGame(game);
    }

    return <React.Fragment>
        <div className="container px-32 flex pt-12">
            <GameCard name="Blicket Experiment (v0)" play_fn={play_fn}></GameCard>
            <GameCard name="Mazes (ICML)" play_fn={play_fn}></GameCard>
        </div>
        {playMode && <div className="fixed top-0 h-screen w-screen">
             <Backdrop onClick={disable_play}/>
             <Launch onClick={disable_play}/>
        </div>}
    </React.Fragment>
}
