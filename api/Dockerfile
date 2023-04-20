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

COPY certificates/* /usr/local/share/ca-certificates/

RUN update-ca-certificates

EXPOSE 3001

CMD [ "npm", "start" ]