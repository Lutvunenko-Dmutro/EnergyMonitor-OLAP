import datetime
import logging
import os

from dotenv import load_dotenv

# --- 1. CONFIGURATION & LOGGING ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("data_generator")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "sslmode": os.getenv("DB_SSL", "prefer"),
}

# --- 2. CONSTANTS & SIMULATION PARAMETERS ---
END_DATE = datetime.datetime.now()
START_DATE = END_DATE - datetime.timedelta(days=90)
FREQ = "60min"

# === 3. LOAD PATTERNS ===
LOAD_PROFILES = {
    "RESIDENTIAL": {
        0: 0.4,
        1: 0.35,
        2: 0.32,
        3: 0.32,
        4: 0.35,
        5: 0.45,
        6: 0.60,
        7: 0.80,
        8: 0.90,
        9: 0.85,
        10: 0.75,
        11: 0.70,
        12: 0.70,
        13: 0.70,
        14: 0.72,
        15: 0.75,
        16: 0.85,
        17: 0.95,
        18: 1.00,
        19: 0.98,
        20: 0.95,
        21: 0.90,
        22: 0.75,
        23: 0.55,
    },
    "INDUSTRIAL": {
        0: 0.60,
        1: 0.55,
        2: 0.55,
        3: 0.55,
        4: 0.58,
        5: 0.65,
        6: 0.75,
        7: 0.85,
        8: 0.95,
        9: 0.98,
        10: 0.98,
        11: 0.98,
        12: 0.90,
        13: 0.95,
        14: 0.98,
        15: 0.98,
        16: 0.95,
        17: 0.85,
        18: 0.75,
        19: 0.70,
        20: 0.65,
        21: 0.60,
        22: 0.60,
        23: 0.60,
    },
    "COMMERCIAL": {
        0: 0.20,
        1: 0.20,
        2: 0.20,
        3: 0.20,
        4: 0.25,
        5: 0.30,
        6: 0.40,
        7: 0.60,
        8: 0.80,
        9: 0.95,
        10: 1.00,
        11: 1.00,
        12: 1.00,
        13: 1.00,
        14: 1.00,
        15: 1.00,
        16: 0.95,
        17: 0.80,
        18: 0.60,
        19: 0.50,
        20: 0.40,
        21: 0.30,
        22: 0.25,
        23: 0.20,
    },
}
