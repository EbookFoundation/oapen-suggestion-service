FROM node:19

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source

COPY . .

COPY ./certificates/* /usr/local/share/ca-certificates/

RUN chmod 644 /usr/local/share/ca-certificates/*.crt && update-ca-certificates

EXPOSE ${API_PORT}

CMD [ "npm", "start" ]
