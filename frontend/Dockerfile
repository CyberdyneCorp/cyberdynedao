# Use Node.js 20 Alpine for smaller image size
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Add python + build tools for node-gyp on Alpine
RUN apk add --no-cache libc6-compat python3 make g++
ENV PYTHON=/usr/bin/python3
WORKDIR /app

# Copy lockfile, manifest, and .npmrc (declares the @cyberdynecorp scope -> GitHub Packages)
COPY package.json package-lock.json* .npmrc ./

# Authenticate to GitHub Packages for the install, then scrub the token so it
# never lands in a layer. NPM_TOKEN must be passed as a build arg (Coolify
# build-arg or `docker build --build-arg NPM_TOKEN=...`).
ARG NPM_TOKEN
RUN echo "//npm.pkg.github.com/:_authToken=${NPM_TOKEN}" >> .npmrc && \
    npm ci && \
    sed -i '/_authToken/d' .npmrc

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

# Contract Addresses
ARG VITE_CYBERDYNE_ACCESS_NFT_ADDRESS

# Cyberdyne backend API base URL (Phase 1+).
# Vite bakes import.meta.env at build time, so this MUST be set as a
# build arg in Coolify (is_build=true), not just a runtime env var.
# When unset the contentApi falls back to bundled static data.
ARG VITE_BACKEND_API_URL

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
    VITE_WEB3AUTH_NETWORK=${VITE_WEB3AUTH_NETWORK} \
    VITE_CYBERDYNE_ACCESS_NFT_ADDRESS=${VITE_CYBERDYNE_ACCESS_NFT_ADDRESS} \
    VITE_BACKEND_API_URL=${VITE_BACKEND_API_URL}

RUN npm run build

# Production image using Nginx to serve static files
FROM nginx:alpine AS runner

# Copy built static files to nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx config. Same-origin reverse proxy for CyberdyneAuth
# means the browser never CORS-preflights and the auth host stays out
# of the Vite bundle.
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
  listen 80;
  server_name localhost;
  root /usr/share/nginx/html;
  index index.html;

  # CyberdyneAuth reverse proxy. Trailing slash on \`proxy_pass\` matters:
  # it tells nginx to strip the \`/api/auth/\` prefix and append the rest
  # to the upstream URL. So /api/auth/api/v1/auth/login forwards as
  # /api/v1/auth/login. (A variable-form proxy_pass disables this URI
  # rewriting — don't switch back to it without adding an explicit
  # \`rewrite\` directive.)
  # ^~ stops nginx from continuing to the static-asset regex location
  # below. Without it, any proxied path whose URI ends in a static
  # extension (e.g. /api/matlab/v1/files/plot_xyz.png) matches the
  # \`\\.(png|js|css|…)$\` regex first and is served from the SPA's
  # html root → 404 with the nginx default HTML page. Auth paths are
  # all JSON today, but mark this ^~ defensively so the same trap
  # can't bite later.
  location ^~ /api/auth/ {
    proxy_pass https://auth.backend.coolify.cyberdynecorp.ai/;
    proxy_set_header Host auth.backend.coolify.cyberdynecorp.ai;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_ssl_server_name on;
    proxy_read_timeout 30s;
    proxy_connect_timeout 10s;
    # Auth tokens are sensitive — never let an intermediary cache them.
    proxy_no_cache 1;
    proxy_cache_bypass 1;
    add_header Cache-Control "no-store" always;
  }

  # MATLAB-LLVM REPL backend reverse proxy. Same trailing-slash trick
  # as /api/auth: the slash on proxy_pass strips the location prefix.
  # The REPL can run for tens of seconds (figure rendering); raise the
  # read timeout accordingly.
  location ^~ /api/matlab/ {
    proxy_pass https://matlab-backend.coolify.cyberdynecorp.ai/;
    proxy_set_header Host matlab-backend.coolify.cyberdynecorp.ai;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_ssl_server_name on;
    proxy_read_timeout 120s;
    proxy_connect_timeout 10s;
    # Plot artifacts can be a few MB — bump the buffer ceiling.
    client_max_body_size 16m;
    proxy_buffering off;
  }

  # Cyberflies (meetings) backend reverse proxy. Same trailing-slash
  # trick as /api/matlab. Audio uploads can be large, so the body-size
  # ceiling is generous; transcription is handled async upstream (the
  # POST returns 202 quickly), but keep a long read timeout for the
  # upload itself over slow links.
  location ^~ /api/cyberflies/ {
    proxy_pass https://cyberflies.backend.coolify.cyberdynecorp.ai/;
    proxy_set_header Host cyberflies.backend.coolify.cyberdynecorp.ai;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_ssl_server_name on;
    proxy_read_timeout 120s;
    proxy_connect_timeout 10s;
    client_max_body_size 256m;
    proxy_buffering off;
  }

  # Python interpreter backend reverse proxy. Code execution can run for
  # tens of seconds; raise the read timeout. Uploaded datasets/artifacts
  # are bounded but can be a few MB.
  location ^~ /api/interpreter/ {
    proxy_pass https://interpreter.backend.coolify.cyberdynecorp.ai/;
    proxy_set_header Host interpreter.backend.coolify.cyberdynecorp.ai;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_ssl_server_name on;
    proxy_read_timeout 120s;
    proxy_connect_timeout 10s;
    client_max_body_size 64m;
    proxy_buffering off;
  }

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

# 127.0.0.1, GET-based (not HEAD), discards body. Required for Coolify+Traefik:
# unhealthy containers get pulled from the upstream pool → 503 to clients.
# See leo-obsidian-vault/Infrastructure/Coolify/Coolify Tricks and Traps.md.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]