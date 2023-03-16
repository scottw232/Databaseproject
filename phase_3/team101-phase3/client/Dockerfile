FROM node:latest

# Create app directory
WORKDIR /usr/src/client

# Install app dependencies
COPY package.json ./

RUN CI=true
RUN npm install
# Bundle app source
COPY . .

# WORKDIR /usr/src/client/src
# RUN ls
# RUN npm install -g create-react-app
# RUN create-react-app reactapp

EXPOSE 3000
CMD ["npm","start"]
