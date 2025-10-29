# Multi-stage Dockerfile for smaller runtime image
FROM node:14 AS builder
WORKDIR /usr/src/app

# Copy package files first to leverage layer caching
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Runtime image
FROM node:14-alpine AS runner
WORKDIR /usr/src/app
ENV NODE_ENV=production

# Copy built artifacts and package.json for production install
COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production

EXPOSE 3000
CMD ["node", "dist/app.js"]