# Copyright (c) 2022 David Chan
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

FROM --platform=linux/amd64 node:16.14.2-alpine AS node_base
FROM --platform=linux/amd64 python:3.8-alpine
COPY --from=node_base / /

# Copy files
RUN mkdir -p /app
COPY ./requirements.txt /app/requirements.txt

# Install python dependencies
RUN cd /app/ && pip install -r requirements.txt

# Install node dependencies
ENV NODE_ENV production
COPY ./asch/react/package.json /tmp/package.json
RUN cd /tmp/ && npm install
RUN mkdir -p /app/asch/react/node_modules && cp -r /tmp/node_modules/* /app/asch/react/

# Copy the main app
WORKDIR /app
COPY . /app

# Link the games to the right location
RUN mkdir /app/asch/react/public/static
RUN ln -s /app/games/ /app/asch/react/public/static/games

# Build the nodejs app
RUN cd /app/asch/react && npm run build

# Install the python app
RUN pip install -e .

# Link the nodejs app to the python server
RUN ln -s /app/asch/react/build/ /app/asch/server/static

# Run the python server
EXPOSE 8080
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "asch.server.server:app"]
