# Build stage
FROM node:20-alpine AS build
WORKDIR /app

ARG VITE_API_BASE

COPY package*.json ./
RUN npm install
COPY . .

# Write the build-time API URL into a real Vite env file - this is Vite's
# officially documented env-loading mechanism, more reliable than relying
# on a plain container ENV var being picked up during the build.
RUN echo "VITE_API_BASE=${VITE_API_BASE}" > .env.production

RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
