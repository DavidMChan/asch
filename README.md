# Asch Experimental Tookit

This is an experimental toolkit for running psychology experiments in unity over the web.

# Running this application

The following steps show how to run the application on any device.

## 1: Creating a Database

This application needs a MongoDB database to function. The easiest way to get a database is to create one with MongoDB's
free [atlas service](https://www.mongodb.com/atlas/database). Once you create a database (and configure access) you will
get a connection string of the form "mongodb+srv://<username>:<password>@<something>.<something>.mongodb.net/?retryWrites=true".

## 2: Build the docker file

Make sure you have [docker](https://docs.docker.com/get-docker/) installed on your machine. You can build the docker file
with `docker build . -t asch:latest`. This may take some time (as there are a lot of dependencies to install), but should
be a relatively automated process.

## 3: Run the docker container

To run the application locally, you can use the following bash command:

```bash
docker run -p 8080:8080 -e ASCH_DATABASE_CONNECTION_STRING="<your connection string>" -e ASCH_FLASK_SECRET_KEY="<a secret key>" asch:latest
```

The server will now be running at `http://localhost:8080`.

# Creating a new game

To create a new game, you need several things:

-   A unity game, which is built, and placed in the "games" directory
-   An experiment file, placed in `asch/server/experiments` which describes the exeperiment.

## Building an integrated unity game

[Coming Soon]

## Building an experiment file

[Coming Soon]
