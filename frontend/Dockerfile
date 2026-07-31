# Build stage
FROM node:20-alpine AS build
WORKDIR /app

# Passed in from docker-compose.yml's build.args, sourced from the root .env
ARG VITE_API_BASE
ENV VITE_API_BASE=$VITE_API_BASE

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve stage - the build output is static files, so a full Node runtime
# isn't needed to serve them, just a lightweight web server.
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
