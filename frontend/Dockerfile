# Use Node.js 20 Alpine for smaller image size
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Add python + build tools for node-gyp on Alpine
RUN apk add --no-cache libc6-compat python3 make g++
ENV PYTHON=/usr/bin/python3
WORKDIR /app

# Copy and install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Build the app
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# ---- BUILD ARGS (from Coolify) ----
# Infura
ARG VITE_INFURA_ENDPOINT

# Base Network
ARG VITE_CHAIN_ID
ARG VITE_NETWORK_NAME
ARG VITE_NATIVE_CURRENCY

# App
ARG VITE_APP_NAME

# Reown / WalletConnect
ARG VITE_REOWN_PROJECT_ID
ARG VITE_REOWN_APP_NAME
ARG VITE_REOWN_APP_DESCRIPTION
ARG VITE_REOWN_APP_URL
ARG VITE_REOWN_APP_ICON

# Web3Auth
ARG VITE_WEB3AUTH_CLIENT_ID
ARG VITE_WEB3AUTH_NETWORK

# ---- Make them visible to the build (Vite reads import.meta.env) ----
ENV VITE_INFURA_ENDPOINT=${VITE_INFURA_ENDPOINT} \
    VITE_CHAIN_ID=${VITE_CHAIN_ID} \
    VITE_NETWORK_NAME="${VITE_NETWORK_NAME}" \
    VITE_NATIVE_CURRENCY=${VITE_NATIVE_CURRENCY} \
    VITE_APP_NAME="${VITE_APP_NAME}" \
    VITE_REOWN_PROJECT_ID=${VITE_REOWN_PROJECT_ID} \
    VITE_REOWN_APP_NAME="${VITE_REOWN_APP_NAME}" \
    VITE_REOWN_APP_DESCRIPTION="${VITE_REOWN_APP_DESCRIPTION}" \
    VITE_REOWN_APP_URL=${VITE_REOWN_APP_URL} \
    VITE_REOWN_APP_ICON=${VITE_REOWN_APP_ICON} \
    VITE_WEB3AUTH_CLIENT_ID=${VITE_WEB3AUTH_CLIENT_ID} \
    VITE_WEB3AUTH_NETWORK=${VITE_WEB3AUTH_NETWORK}

RUN npm run build

# Production image using Nginx to serve static files
FROM nginx:alpine AS runner

# Copy built static files to nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx config
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
  listen 80;
  server_name localhost;
  root /usr/share/nginx/html;
  index index.html;

  location / { try_files \$uri \$uri/ /index.html; }

  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header X-XSS-Protection "1; mode=block" always;

  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }
  location ~* \.html$ {
    expires -1;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
  }
}
EOF

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]