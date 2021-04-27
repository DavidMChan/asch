#!/bin/bash

if [ -f "src/.cache/tailwind.css" ]; then
    STATUS="$(cmp --silent src/.cache/tailwind.css src/tailwind.css; echo $?)"  # "$?" gives exit status for each comparison
    if [[ $STATUS -ne 0 ]]; then
        mkdir -p "src/.cache"
        cp src/tailwind.css src/.cache/tailwind.css
        tailwindcss build src/tailwind.css -o src/tailwind.output.css
    else
        echo "Tailwind CSS file unchanged. Not rebuilding."
    fi
else
    mkdir -p "src/.cache"
    cp src/tailwind.css src/.cache/tailwind.css
    tailwindcss build src/tailwind.css -o src/tailwind.output.css
fi
