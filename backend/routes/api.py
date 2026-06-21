from flask import Blueprint, request, jsonify, send_file, url_for
from services.data_access import (
    fetch_attempts, fetch_history, fetch_cases,
    insert_history, fetch_logs, fetch_steps,
    sync_attempts_from_vm_a, get_local_summary, get_moodle_summary
)
from services.predictor import analyze_attempts
from services.threshold_manager import get_thresholds, set_thresholds
from services.auth import require_auth
from services.notifier import notify_proctors
from config import Config
import os
import jwt
import datetime
from cryptography.hazmat.primitives import serialization

api_bp = Blueprint('api', __name__)

# ------------------------------------------------------------
# 1. Analisis peserta & deteksi kecurangan
# ------------------------------------------------------------
@api_bp.route('/daftar_peserta', methods=['GET'])
@require_auth
def daftar_peserta():
    """
    Analisis Peserta & Deteksi Kecurangan
    ---
    tags:
      - Deteksi Kecurangan
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Daftar peserta dengan status hasil analisis
        schema:
          type: array
          items:
            type: object
            properties:
              userid:
                type: string
                example: "12345"
              firstname:
                type: string
                example: "Budi"
              lastname:
                type: string
                example: "Santoso"
              status:
                type: string
                enum: ["aman", "terindikasi"]
                example: "terindikasi"
              session:
                type: string
                example: "listening"
              timestart:
                type: string
                example: "08:00:00"
              timefinish:
                type: string
                example: "08:15:00"
              timetaken:
                type: string
                example: "00:15:00"
              score:
                type: number
                example: 85
      401:
        description: Unauthorized - API Key tidak valid
    """
    session, df = fetch_attempts()
    results = analyze_attempts(df, session)

    for r in results:
        insert_history(r)

    cheating_cases = [r for r in results if r['status'] == 'terindikasi']
    if cheating_cases:
        notify_proctors(cheating_cases, session)

    return jsonify(results)


# ------------------------------------------------------------
# 2. Riwayat peserta
# ------------------------------------------------------------
@api_bp.route('/peserta_history', methods=['GET'])
@require_auth
def peserta_history():
    """
    Riwayat Peserta (History)
    ---
    tags:
      - History
    security:
      - ApiKeyAuth: []
    parameters:
      - name: query
        in: query
        type: string
        required: false
        description: "Nama peserta yang dicari (contoh: 'Budi')"
    responses:
      200:
        description: Data riwayat peserta dari tabel history
        schema:
          type: array
          items:
            type: object
            properties:
              userid:
                type: string
              firstname:
                type: string
              lastname:
                type: string
              score:
                type: integer
              status:
                type: string
              session:
                type: string
      401:
        description: Unauthorized
    """
    query = request.args.get('query', '')
    data = fetch_history(query)
    return jsonify(data)


# ------------------------------------------------------------
# 3. Ringkasan statistik lokal
# ------------------------------------------------------------
@api_bp.route('/get_summary', methods=['GET'])
@require_auth
def get_summary():
    """
    Ringkasan Statistik Lokal
    ---
    tags:
      - Summary
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Ringkasan total case, label, user, dan monthly dari database lokal
        schema:
          type: object
          properties:
            total_case:
              type: integer
              example: 15
            total_label_0:
              type: integer
              example: 200
            total_label_1:
              type: integer
              example: 15
            total_user:
              type: integer
              example: 215
            total_case_monthly:
              type: array
              items:
                type: object
      401:
        description: Unauthorized
    """
    summary = get_local_summary()
    return jsonify(summary)


# ------------------------------------------------------------
# 4. Daftar kasus kecurangan yang tersimpan
# ------------------------------------------------------------
@api_bp.route('/api/get_cases', methods=['GET'])
@require_auth
def get_cases():
    """
    Daftar Kasus Kecurangan Tersimpan
    ---
    tags:
      - Cases
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Daftar seluruh kasus kecurangan yang pernah tercatat
        schema:
          type: array
          items:
            type: object
            properties:
              userid:
                type: string
              firstname:
                type: string
              lastname:
                type: string
              status:
                type: string
                example: "terindikasi"
              session:
                type: string
              shift:
                type: string
      401:
        description: Unauthorized
    """
    cases = fetch_cases()
    return jsonify(cases)


# ------------------------------------------------------------
# 5. Detail peserta (anonim)
# ------------------------------------------------------------
@api_bp.route('/detail_peserta', methods=['GET'])
@require_auth
def detail_peserta():
    """
    Detail Peserta (Teraanonimisasi)
    ---
    tags:
      - Deteksi Kecurangan
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Data peserta dengan nama anonim untuk tampilan publik
        schema:
          type: array
          items:
            type: object
            properties:
              userid:
                type: string
              firstname:
                type: string
                example: "user"
              lastname:
                type: string
                example: "name_1"
              status:
                type: string
                enum: ["honest", "possibly cheating"]
              session:
                type: string
              timetaken:
                type: string
              score:
                type: number
      401:
        description: Unauthorized
    """
    session, df = fetch_attempts()
    results = analyze_attempts(df, session)

    sanitized = []
    for r in results:
        item = dict(r)
        if r['status'] == 'aman':
            item['firstname'] = 'user'
            item['lastname'] = 'name_1'
            item['status'] = 'honest'
        else:
            item['firstname'] = 'user'
            item['lastname'] = 'name_2'
            item['status'] = 'possibly cheating'
        sanitized.append(item)

    return jsonify(sanitized)


# ------------------------------------------------------------
# 6. Pengaturan threshold
# ------------------------------------------------------------
@api_bp.route('/treshold-settings', methods=['POST'])
@require_auth
def threshold_settings():
    """
    Pengaturan Threshold Deteksi
    ---
    tags:
      - Settings
    security:
      - ApiKeyAuth: []
    parameters:
      - name: listening-timetaken
        in: query
        type: integer
        required: false
        description: "Threshold waktu listening (menit)"
      - name: listening-minscore
        in: query
        type: integer
        required: false
        description: "Threshold skor minimal listening"
      - name: grammar-timetaken
        in: query
        type: integer
        required: false
        description: "Threshold waktu grammar (menit)"
      - name: grammar-minscore
        in: query
        type: integer
        required: false
        description: "Threshold skor minimal grammar"
      - name: reading-timetaken
        in: query
        type: integer
        required: false
        description: "Threshold waktu reading (menit)"
      - name: reading-minscore
        in: query
        type: integer
        required: false
        description: "Threshold skor minimal reading"
    responses:
      200:
        description: Threshold berhasil diperbarui
        schema:
          type: object
          properties:
            listening_timetaken:
              type: integer
            listening_minscore:
              type: integer
            grammar_timetaken:
              type: integer
            grammar_minscore:
              type: integer
            reading_timetaken:
              type: integer
            reading_minscore:
              type: integer
      401:
        description: Unauthorized
    """
    new_settings = {
        'listening_timetaken': request.args.get('listening-timetaken', 0, type=int) * 60,
        'listening_minscore': request.args.get('listening-minscore', 0, type=int),
        'grammar_timetaken': request.args.get('grammar-timetaken', 0, type=int) * 60,
        'grammar_minscore': request.args.get('grammar-minscore', 0, type=int),
        'reading_timetaken': request.args.get('reading-timetaken', 0, type=int) * 60,
        'reading_minscore': request.args.get('reading-minscore', 0, type=int),
    }
    set_thresholds(new_settings)
    return jsonify(new_settings)


# ------------------------------------------------------------
# 7. Sinkronisasi data attempt
# ------------------------------------------------------------
@api_bp.route('/sync-attempts', methods=['POST'])
@require_auth
def sync_attempts():
    """
    Sinkronisasi Data Attempt dari VM-A ke VM-B
    ---
    tags:
      - Sync
    security:
      - ApiKeyAuth: []
    parameters:
      - name: start_time
        in: query
        type: integer
        required: true
        description: "UNIX timestamp awal (contoh: 1700000000)"
      - name: end_time
        in: query
        type: integer
        required: true
        description: "UNIX timestamp akhir (contoh: 1700100000)"
    responses:
      200:
        description: Berhasil sinkronisasi
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            rows_synced:
              type: integer
              example: 42
      400:
        description: Parameter tidak lengkap
      401:
        description: Unauthorized
    """
    start_time = request.args.get('start_time', type=int)
    end_time = request.args.get('end_time', type=int)
    if not start_time or not end_time:
        return jsonify({"error": "start_time and end_time required"}), 400
    rows_synced = sync_attempts_from_vm_a(start_time, end_time)
    return jsonify({"status": "success", "rows_synced": rows_synced})


# ------------------------------------------------------------
# 8. Log aktivitas VM-A
# ------------------------------------------------------------
@api_bp.route('/get/logs', methods=['GET'])
@require_auth
def get_logs():
    """
    Log Aktivitas Moodle (VM-A)
    ---
    tags:
      - Logs
    security:
      - ApiKeyAuth: []
    parameters:
      - name: start_time
        in: query
        type: integer
        required: true
        description: "UNIX timestamp awal"
      - name: end_time
        in: query
        type: integer
        required: true
        description: "UNIX timestamp akhir"
    responses:
      200:
        description: Array log aktivitas
        schema:
          type: array
          items:
            type: object
      400:
        description: Parameter tidak lengkap
      401:
        description: Unauthorized
    """
    start_time = request.args.get('start_time', type=int)
    end_time = request.args.get('end_time', type=int)
    if not start_time or not end_time:
        return jsonify({"error": "start_time and end_time required"}), 400
    logs = fetch_logs(start_time, end_time)
    return jsonify(logs)


# ------------------------------------------------------------
# 9. Step data (waktu per soal)
# ------------------------------------------------------------
@api_bp.route('/user-steps', methods=['GET'])
@require_auth
def user_steps():
    """
    Data Langkah Pengerjaan Soal (Step Data)
    ---
    tags:
      - Step Data
    security:
      - ApiKeyAuth: []
    parameters:
      - name: course_id
        in: query
        type: integer
        required: false
        default: 4
        description: "ID course di Moodle"
      - name: limit
        in: query
        type: integer
        required: false
        default: 100
        description: "Batas jumlah data yang dikembalikan"
    responses:
      200:
        description: Data langkah per soal
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            data:
              type: array
              items:
                type: object
      401:
        description: Unauthorized
    """
    course_id = request.args.get('course_id', type=int, default=4)
    limit = request.args.get('limit', type=int, default=100)
    steps = fetch_steps(course_id, limit)
    return jsonify({'status': 'success', 'data': steps})


# ------------------------------------------------------------
# 10. Ringkasan dashboard dari VM-A
# ------------------------------------------------------------
@api_bp.route('/summary', methods=['GET'])
@require_auth
def dashboard_summary():
    """
    Ringkasan Dashboard dari VM-A (Moodle)
    ---
    tags:
      - Summary
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Statistik Moodle (total user, log, steps, direktori backup)
        schema:
          type: object
          properties:
            count_users:
              type: integer
              example: 1500
            count_mdl_standard_logs:
              type: integer
              example: 45000
            count_total_steps:
              type: integer
              example: 12000
            count_directory:
              type: integer
              example: 5
      401:
        description: Unauthorized
    """
    summary = get_moodle_summary()
    return jsonify(summary)


# ------------------------------------------------------------
# 11. Backup file explorer & download
# ------------------------------------------------------------
@api_bp.route('/directory', defaults={'subdir': ''})
@api_bp.route('/directory/<path:subdir>')
@require_auth
def list_backups(subdir):
    """
    Eksplorasi Direktori Backup
    ---
    tags:
      - Backup Files
    security:
      - ApiKeyAuth: []
    parameters:
      - name: subdir
        in: path
        type: string
        required: false
        description: "Subdirektori di dalam folder backup"
    responses:
      200:
        description: Daftar file dan folder di dalam direktori
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
              fullpath:
                type: string
              url:
                type: string
      403:
        description: Path tidak valid
      404:
        description: Direktori tidak ditemukan
    """
    base_dir = Config.BACKUP_DIR
    full_path = os.path.normpath(os.path.join(base_dir, subdir))

    if not full_path.startswith(os.path.normpath(base_dir)):
        return jsonify({"error": "Invalid path"}), 403
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        return jsonify({"error": "Directory not found"}), 404

    files = []
    for entry in os.listdir(full_path):
        entry_path = os.path.join(full_path, entry)
        if os.path.isfile(entry_path):
            file_url = url_for('api.download_file',
                               filename=os.path.join(subdir, entry),
                               _external=True)
            files.append({
                "title": entry,
                "fullpath": entry_path,
                "url": file_url
            })
        elif os.path.isdir(entry_path):
            dir_url = url_for('api.list_backups',
                              subdir=os.path.join(subdir, entry),
                              _external=True)
            files.append({
                "title": entry + "/",
                "fullpath": entry_path,
                "url": dir_url
            })
    return jsonify(files)


@api_bp.route('/download/<path:filename>')
@require_auth
def download_file(filename):
    """
    Unduh File Backup
    ---
    tags:
      - Backup Files
    security:
      - ApiKeyAuth: []
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: "Path relatif file yang akan diunduh"
    produces:
      - application/octet-stream
    responses:
      200:
        description: File binary
      403:
        description: Path tidak valid
      404:
        description: File tidak ditemukan
    """
    file_path = os.path.normpath(os.path.join(Config.BACKUP_DIR, filename))
    if not file_path.startswith(os.path.normpath(Config.BACKUP_DIR)):
        return jsonify({"error": "Invalid path"}), 403
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)


# ------------------------------------------------------------
# 12. JWKS Endpoint (public key)
# ------------------------------------------------------------
@api_bp.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    """
    JWKS Endpoint
    ---
    tags:
      - Auth
    responses:
      200:
        description: Public key dalam format JWKS
    """
    from services.auth import get_jwks
    return jsonify(get_jwks())


# ------------------------------------------------------------
# 13. Penerbitan JWT Token (menggunakan API Key)
# ------------------------------------------------------------
@api_bp.route('/auth/token', methods=['POST'])
@require_auth
def generate_token():
    """
    Menerbitkan JWT untuk Client
    ---
    tags:
      - Auth
    security:
      - ApiKeyAuth: []
    parameters:
      - name: role
        in: query
        type: string
        required: false
        default: "proctor"
        description: "Peran untuk token (proctor/admin)"
    responses:
      200:
        description: JWT token
        schema:
          type: object
          properties:
            access_token:
              type: string
            token_type:
              type: string
              example: "bearer"
      401:
        description: Unauthorized
    """
    role = request.args.get('role', 'proctor')

    # Baca private key dari file
    with open('keys/private.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    payload = {
        "sub": "client",
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return jsonify({"access_token": token, "token_type": "bearer"})