# ==============================================
# Stage 1: Build aplikasi Vue
# ==============================================
FROM node:18-alpine AS build-stage

WORKDIR /app

# Salin file package.json dan lock terlebih dahulu (agar cache npm efektif)
COPY package*.json ./

# Install dependensi
RUN npm ci --only=production

# Salin seluruh kode sumber
COPY . .

# Build aplikasi ke folder dist
RUN npm run build

# ==============================================
# Stage 2: Serve dengan Nginx (ringan)
# ==============================================
FROM nginx:alpine

# Salin hasil build dari stage sebelumnya ke direktori html Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Salin konfigurasi Nginx custom (opsional, untuk SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Ekspos port 80
EXPOSE 80

# Nginx sudah otomatis berjalan
CMD ["nginx", "-g", "daemon off;"]