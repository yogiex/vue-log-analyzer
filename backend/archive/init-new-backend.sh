#!/bin/bash

# Script untuk membuat struktur folder dan file kosong untuk proyek backend baru
# Jalankan dari dalam folder backend/ (yang saat ini hanya berisi backup-files/)
# Folder backup-files tidak akan disentuh

set -e

echo "🚀 Membuat struktur proyek backend baru..."

# Pastikan kita berada di direktori backend/
if [ ! -d "backup-files" ]; then
    echo "❌ Folder 'backup-files' tidak ditemukan. Jalankan script dari dalam folder backend/"
    exit 1
fi

# Buat folder-folder utama
mkdir -p models
mkdir -p scripts/bash
mkdir -p scripts/sql
mkdir -p templates
mkdir -p static
mkdir -p tests
mkdir -p backup-file/downloaded_files
mkdir -p archive

# Buat file-file utama (kosong)
touch app.py
touch config.py
touch requirements.txt
touch Dockerfile
touch docker-compose.yml
touch README.md

# File pendukung
touch .env.example
touch .gitignore

# Isi .gitignore dengan pola dasar (opsional, bisa dikosongkan)
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
*.log
backup-file/
EOF

# Buat file statis dan template awal
touch static/styles.css
touch templates/index.html
touch templates/usernames.html

# Buat file pengujian awal
touch tests/__init__.py
touch tests/test_app.py

# Buat script placeholder
touch scripts/bash/export-sql.sh
touch scripts/sql/attempt.sql
touch scripts/sql/log.sql
touch scripts/sql/step.sql

# Beri izin eksekusi pada script bash (kosong, tapi bisa diisi nanti)
chmod +x scripts/bash/export-sql.sh

echo "✅ Struktur baru berhasil dibuat."
echo "   Folder 'backup-files' tetap utuh sebagai arsip."
echo ""
echo "📁 Struktur saat ini:"
tree -L 2