# Use official Node.js image as the base image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

COPY .envDocker .env

# Build the Next.js application


# Expose the port on which your Next.js app will run
EXPOSE 3000

RUN npm run build

# Command to start the application
CMD ["npm", "run", "start"]