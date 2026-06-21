# skills-markdown.md — Aturan Penulisan Markdown untuk AI & Developer

Dokumen ini adalah **panduan wajib** bagi seluruh tim (termasuk agen AI seperti opencode) saat membuat, mengedit, atau memvalidasi file `*.md` dalam proyek ini. Tujuannya adalah memastikan semua dokumentasi (termasuk `UIUX.md`, `README.md`, dan spesifikasi teknis) memiliki kualitas, akurasi, dan konsistensi yang tinggi.

---

## 1. Tujuan & Filosofi

- **Akurasi Teknis > Gaya Menulis** – Dokumentasi yang salah secara teknis lebih berbahaya daripada dokumen yang ditulis dengan tata bahasa buruk.
- **Keseragaman Struktur** – Semua file Markdown harus mudah dipindai (scannable) oleh manusia dan diparsing oleh AI.
- **Actionable** – Setiap aturan atau panduan harus dapat langsung diterapkan ke kode (copy-paste ready).
- **Version-Aware** – Karena proyek menggunakan Vue 3 + Vuetify 3, semua contoh kode WAJIB mengikuti sintaks versi terbaru.

---

## 2. Aturan Emas: Validasi Teknis (Golden Rule)

> **JANGAN PERNAH menulis properti, kelas, atau komponen Vuetify hanya berdasarkan ingatan (memory) model.**  
> Setiap kali menulis kode atau aturan yang berkaitan dengan **Vuetify, Vue 3, atau library eksternal**, WAJIB melakukan validasi silang dengan dokumentasi resmi.

### 2.1 Proses Validasi Wajib

1. **Cek dokumentasi resmi**:
   - Vuetify 3: [https://vuetifyjs.com/en/](https://vuetifyjs.com/en/)
   - Vue 3: [https://vuejs.org/](https://vuejs.org/)
   - Library lain (Chart.js, Firebase, dll): cek docs masing-masing.
2. **Prioritaskan Migration Guide** – Jika ragu antara Vuetify 2 dan 3, buka [Migration Guide from Vuetify 2 to 3](https://vuetifyjs.com/en/introduction/upgrade-guide/).
3. **Cek contoh kode** – Pastikan snippet yang ditulis di dokumentasi benar-benar berfungsi di environment proyek.

### 2.2 Contoh Kesalahan yang Harus Dihindari

| ❌ Salah (Vuetify 2)               | ✅ Benar (Vuetify 3)                          |
| ---------------------------------- | --------------------------------------------- |
| `class="text-h4"`                  | `class="text-headline-medium"`                |
| `variant="flat"` (untuk primary)   | `variant="elevated"` (default primary)        |
| `v-data-table` slot `header.<key>` | Gunakan slot `headers` atau `item.<key>`      |
| `item-class` prop                  | Gunakan `row-props` atau kustomisasi via slot |

---

## 3. Struktur & Tata Letak File

### 3.1 Frontmatter (Opsional tapi Direkomendasikan)

Setiap file Markdown utama (seperti `UIUX.md`) HARUS diawali dengan metadata:

```markdown
# Judul Utama — Deskripsi Singkat

**Versi**: 1.0.0  
**Terakhir Diperbarui**: YYYY-MM-DD  
**Status**: `Aktif` | `Draft` | `Arsip`  
**Berlaku untuk**: Vue 3 + Vuetify 3
```

### 3.2 Daftar Isi (Table of Contents)

Untuk file dengan panjang > 500 kata, WAJIB menyertakan daftar isi:

```markdown
## Daftar Isi

1. [Filosofi](#1-filosofi)
2. [Aturan Emas](#2-aturan-emas)
3. [Struktur](#3-struktur--tata-letak-file)
   - 3.1 [Frontmatter](#31-frontmatter)
   - 3.2 [Daftar Isi](#32-daftar-isi)
     ...
```

### 3.3 Hierarki Heading

Gunakan ATX headings (`#`) dengan aturan:

- `#` – Hanya untuk judul utama file.
- `##` – Bagian utama (section).
- `###` – Sub-bagian.
- `####` – Detail spesifik (contoh, properti komponen).
- **Maksimal 5 level** (`#####`), hindari lebih dalam.

---

## 4. Gaya Penulisan

- **Bahasa**: Gunakan **Bahasa Indonesia** untuk narasi umum, tetapi **pertahankan istilah teknis dalam bahasa Inggris** (misal: _button, prop, component, slot, event_).
- **Nada**: Imperatif, jelas, dan langsung. Hindari kalimat pasif yang bertele-tele.
  - ❌ "Diharapkan untuk tidak melakukan hardcode hex value."
  - ✅ "Jangan hardcode hex value."
- **Kata Baku**: Gunakan istilah yang konsisten.
  - `komponen` (bukan _component_ jika dalam kalimat Indonesia).
  - `properti` atau `props` (konsisten, pilih salah satu dan gunakan di seluruh dokumen).

---

## 5. Tabel (Tables)

Gunakan tabel untuk data terstruktur (token, properti, ukuran, dll). **Pastikan tabel memiliki header** dan rata kiri untuk teks, rata kanan untuk angka jika perlu.

### Format Baku:

```markdown
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Konten A | Konten B | 123      |
| Konten C | Konten D | 456      |
```

### Aturan Tambahan:

- Jangan gunakan tabel untuk narasi panjang (lebih baik gunakan daftar berpoin).
- Jika nilai berupa kode, gunakan backtick di dalam sel (contoh: `variant="elevated"`).

---

## 6. Blok Kode (Code Snippets)

### 6.1 Spesifikasi Bahasa

WAJIB mencantumkan jenis bahasa setelah backtick pembuka:

````markdown
\```vue
<template>
<v-btn color="primary">Simpan</v-btn>
</template>
\```

\```scss
.dashboard-card { border-radius: 8px; }
\```

\```javascript
const user = ref(null);
\```

\```bash
npm install @mdi/font
\```
````

### 6.2 Kelengkapan Snippet

- Snippet Vue WAJIB menunjukkan bagian yang relevan (`<template>`, `<script setup>`, atau `<style>`).
- Jangan menulis snippet yang "hampir benar"; pastikan kode dapat langsung di-copy-paste tanpa error sintaks.
- Tambahkan komentar `// ... ` untuk bagian yang dihilangkan agar tidak membingungkan.

### 6.3 Highlighting

Gunakan **tebal** (`**...**`) untuk menekankan kata kunci dalam teks biasa.  
Gunakan `backticks` untuk menyebut nama properti, kelas, atau variabel di dalam kalimat.

Contoh:

> Gunakan prop `density="comfortable"` pada `v-data-table` untuk tampilan yang lebih rapat.

---

## 7. Referensi & Tautan

- **Tautan Internal**: Gunakan relative path (contoh: `[UIUX.md](./UIUX.md)`).
- **Tautan Eksternal**: Gunakan teks deskriptif, bukan URL mentah.
  - ❌ `https://vuetifyjs.com/en/styles/typography/`
  - ✅ `[Dokumentasi Tipografi Vuetify 3](https://vuetifyjs.com/en/styles/typography/)`
- **Cross-Reference**: Jika merujuk ke bagian lain dalam file yang sama, gunakan anchor link:
  - `[Lihat aturan spasi](#4-spasi--layout)`

---

## 8. Daftar (Lists)

- Gunakan **unordered list** (`-` atau `*`) untuk poin yang tidak memiliki urutan prioritas.
- Gunakan **ordered list** (`1.`, `2.`) untuk langkah-langkah prosedural.
- Jangan campur gaya list dalam satu blok.

### 8.1 Daftar Bersarang

Indentasi dengan **2 spasi** (bukan tab) untuk sub-poin:

```markdown
- Komponen Utama:
  - `v-btn`: Untuk tombol aksi.
  - `v-card`: Untuk wadah konten.
    - Gunakan `elevation="2"` sebagai default.
```

---

## 9. Callouts / Kutipan Khusus

Gunakan blockquote (`>`) untuk:

- Peringatan penting (Warning)
- Catatan khusus (Note)
- Best practice yang tidak boleh dilanggar

### Format:

```markdown
> **⚠️ Peringatan**: Jangan pernah menggunakan `!important` di CSS kustom.

> **💡 Catatan**: Vuetify 3 mendukung dark mode secara otomatis jika tema dikonfigurasi dengan benar.
```

---

## 10. Checklist Validasi Mandiri (Untuk AI & Reviewer)

Sebelum menyelesaikan atau meng-_commit_ file `*.md`, pastikan:

- [ ] **Akurasi**: Semua kelas/properti Vuetify 3 sudah diverifikasi dengan dokumentasi resmi.
- [ ] **Ejaan & Tata Bahasa**: Tidak ada typo pada istilah teknis.
- [ ] **Struktur**: Ada Daftar Isi untuk file panjang, hierarki heading sesuai.
- [ ] **Snippet**: Semua kode memiliki label bahasa dan siap pakai.
- [ ] **Konsistensi**: Istilah yang sama digunakan secara konsisten di seluruh dokumen.
- [ ] **Tautan**: Tidak ada tautan rusak (pastikan anchor link sesuai dengan judul heading).

---

## 11. Contoh Penerapan di `UIUX.md` (Studi Kasus)

Dokumen `UIUX.md` sebelumnya memiliki kesalahan karena menulis `text-h4` (Vuetify 2).  
Dengan aturan ini, penulis HARUS membuka [halaman Typography Vuetify 3](https://vuetifyjs.com/en/styles/typography/) dan menulis ulang menjadi:

```markdown
| Element       | Vuetify 3 Class        | Size |
| ------------- | ---------------------- | ---- |
| Page Title    | `text-headline-medium` | 28px |
| Section Title | `text-headline-small`  | 24px |
```

---

**Dokumen ini adalah panduan wajib.** Setiap pelanggaran terhadap aturan teknis (khususnya Vuetify 3) akan dianggap sebagai _bug dokumentasi_ dan harus diperbaiki segera.
