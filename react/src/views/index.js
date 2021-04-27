import React from 'react';
import {
    Link
} from "react-router-dom";

export default function Index() {
    return (
        <div className="container">
            <figure className="flex bg-gray-100 rounded-xl p-8">
            <img className="w-32 h-32 rounded-full mx-auto" src="https://picsum.photos/200/300" alt="" width="384" height="512" />
            <br />
            <div className="pt-6 p-8 text-center space-y-4">
                <blockquote>
                <p className="text-lg font-semibold">
                    “Tailwind CSS is the only framework that I've seen scale
                    on large teams. It’s easy to customize, adapts to any design,
                    and the build size is tiny.”
                </p>
                </blockquote>
                <figcaption className="font-medium">
                <div className="text-cyan-600">
                    Sarah Dayan
                </div>
                <div className="text-gray-500">
                    Staff Engineer, Algolia
                </div>
                </figcaption>
            </div>
            </figure>
        </div>
    )
}