from services.database import get_source_db, get_moodle_db
import pandas as pd

def fetch_attempts():
    # Ambil data attempt yang belum diproses? Atau dengan filter waktu.
    # Gunakan parameterized query, misal hanya yang timestart dalam rentang tertentu.
    conn = get_source_db()
    query = """
        SELECT id_peserta, firstname, lastname, quiz_name, unique_id, timestart, timefinish, score
        FROM backup_attempt
        WHERE timefinish >= NOW() - INTERVAL 1 HOUR
    """
    df = pd.read_sql(query, conn)
    conn.close()
    # Tentukan sesi dari quiz_name
    session = detect_session(df)
    return session, df

def detect_session(df):
    # implementasi logika penentuan session dari nama kuis
    ...