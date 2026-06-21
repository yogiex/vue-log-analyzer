import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database VM-A (Moodle)
    DB_VM_A = {
        'host': os.getenv('MYSQL_HOST_VM_A'),
        'user': os.getenv('MYSQL_USER_VM_A'),
        'password': os.getenv('MYSQL_PASS_VM_A'),
        'database': os.getenv('MYSQL_DB_VM_A')
    }

    # Database VM-B (backup/source untuk analisis)
    DB_SOURCE = {
        'host': os.getenv('hostname_source'),
        'user': os.getenv('db_username_source'),
        'password': os.getenv('password_source'),
        'database': os.getenv('database_source')
    }

    # Telegram Bot
    TELEGRAM_TOKEN = os.getenv('TOKEN_BOT_TELEGRAM')

    # Model paths
    MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
    MODEL_GRAMMAR = os.path.join(MODEL_DIR, 'Grammar_iso_forest_model.pkl')
    MODEL_LISTENING = os.path.join(MODEL_DIR, 'Listening_iso_forest_model.pkl')
    MODEL_READING = os.path.join(MODEL_DIR, 'Reading_iso_forest_model.pkl')

    # Threshold dinamis (default)
    DEFAULT_THRESHOLDS = {
        'listening_timetaken': 0,
        'listening_minscore': 0,
        'grammar_timetaken': 0,
        'grammar_minscore': 0,
        'reading_timetaken': 0,
        'reading_minscore': 0
    }

    # Path backup
    BACKUP_DIR = '/home/linux/backup-sql'