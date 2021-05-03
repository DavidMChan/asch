import React, { useState } from 'react';
import {
    Link
} from "react-router-dom";
import { Card, CardBody, Button } from '@windmill/react-ui'

function Launch(props) {
    return  <div className="flex items-center justify-center h-screen z-50 w-screen relative" onClick={props.onClick}>
                <div className="bg-indigo-800 text-white font-bold rounded-lg border shadow-lg p-10">
                    Centered Content
                </div>
            </div>;
}


function GameCard(props) {

    return (<div class="w-full p-3">
                <div class="flex flex-col rounded overflow-hidden h-auto border shadow-lg">
                    <img class="block h-auto flex-none bg-cover" src={`https://picsum.photos/seed/${props.name}/800`} />
                    <div class="bg-white rounded-b p-4 flex flex-col justify-center text-center leading-normal">
                        <div class="text-black font-bold text-xl mb-2 leading-tight">{props.name}</div>
                        <button class="m-3 h-10 text-base font-semibold rounded-full block border-2 border-purple-300 hover:bg-purple-300 text-purple-700"
                                type="button"
                                onClick={() => {window.location.href = `${window.location.protocol}//${window.location.host}/play?experiment=${props.experiment}`}}>Play</button>
                        <button class="m-3 h-10 text-base font-semibold rounded-full block border-2 border-purple-300 hover:bg-purple-300 text-purple-700">Manage</button>
                    </div>
                </div>
            </div>);

}


export default function Index() {
    return <React.Fragment>

        <div className="h-screen w-screen">
            <div className="p-10">
                <h1 className="text-center text-4xl">Asch Experimentation Server @ UC Berkeley</h1>
            </div>
            <div className="h-100 w-100 grid grid-cols-1 md:grid-cols-2 gap-4 justify-evenly justify-items-center p-20">
                <GameCard name="Blicket Experiment (v0)" experiment="blicket"></GameCard>
                <GameCard name="Mazes (ICML)" experiment="icml_maze"></GameCard>
            </div>
        </div>
    </React.Fragment>
}
