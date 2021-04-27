import React from 'react';
import {
    Link
} from "react-router-dom";


function GameCard(props) {
    return (<div className="w-full max-w-full flex p-4">
                <div className="h-auto w-48 bg-cover rounded-t text-center overflow-hidden"
                     style={{backgroundImage: "url('https://picsum.photos/200')"}}>
                </div>
                <div class="border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t lg:border-gray-400 bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
                    <div class="mb-8 justify-center">
                        <div class="text-gray-900 font-bold text-xl mb-2">{props.name}</div>
                        <button class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-full shadow-lg mt-2"> Play </button> <br />
                        <button class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-full shadow-lg mt-4"> Manage / View Results </button>
                    </div>
                </div>
            </div>)
}


export default function Index() {
    return (
        <div className="container px-32 flex pt-12">
            <GameCard name="Blicket Experiment (v0)"></GameCard>
            <GameCard name="Mazes (ICML)"></GameCard>
        </div>
    )
}
