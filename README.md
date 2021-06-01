# Asch Experimental Tookit

This is an experimental toolkit for running psychology experiments in unity over the web.

# Installation Instructions


##  Install the games

If you have a unity build, place it in the server folder as follows:
```
asch
  server
    static
      games
        <game build path>
          Build
            unity.data
            unity.framework.js
            unity.loader.js
            unity.wasm
          TemplateData
            ...
          index.html
```

## Build the React App

1. Install the package requirements by changing into the `asch/react/` folder and running `npm install`
2. Build the react app with `npm run build`

## Run the server

1. Run `pip install -e .` in the home directory to install the server package.
2. Create an `~/.aschrc` file with the following configuration keys:

```
[database]
connection_string = <YOUR MONGODB CONNECTION STRING>
[flask]
secret_key = <A STRING TO USE FOR FLASK
```

3. Run `python asch/server/server.py` to run the server
