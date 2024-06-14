# Use an Ubuntu base image
FROM ubuntu:20.04

# Install Python and Node.js
RUN apt-get update && \
    apt-get install -y python3.8 python3-pip curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the Python requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Install Node dependencies
ENV NODE_ENV production
COPY ./asch/react/package.json /tmp/package.json
RUN cd /tmp/ && npm install
RUN mkdir -p /app/asch/react/ && mv /tmp/node_modules /app/asch/react/

# Copy the main app
COPY . /app

# Link the games to the right location
RUN mkdir /app/asch/react/public/static
RUN ln -s /app/games/ /app/asch/react/public/static/games

# Build the Node.js app
RUN cd /app/asch/react && npm run build

# Install the Python app
RUN pip3 install -e .

# Link the Node.js app to the Python server
RUN ln -s /app/asch/react/build/ /app/asch/server/static

# Expose port 8080 for the server
EXPOSE 8080

# Command to run the server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "asch.server.server:app"]

