from ..configurations import *
from ..logger import *


class HashDatabase:
    """Handles local SQLite database for malicious SHA256 hashes."""

    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self._create_table()

    def _create_table(self):
        """Create database table if not exists."""
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS hashes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sha256 TEXT UNIQUE
                )
            """)
            self.conn.commit()

    def insert_many(self, hashes):
        """Insert multiple hashes safely into the database."""
        with self.lock:
            cur = self.conn.cursor()
            cur.executemany(
                "INSERT OR IGNORE INTO hashes (sha256) VALUES (?)",
                [(h.strip(),) for h in hashes if len(h.strip()) == 64]
            )
            self.conn.commit()

    def exists(self, sha256):
        """Check if a hash exists in the database."""
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("SELECT 1 FROM hashes WHERE sha256 = ?", (sha256,))
            return cur.fetchone() is not None

    def count(self):
        """Return total number of hashes stored."""
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM hashes")
            return cur.fetchone()[0]

