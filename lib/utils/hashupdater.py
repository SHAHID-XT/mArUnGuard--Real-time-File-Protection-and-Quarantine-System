from ..configurations import *
from ..logger import *
from lib.utils.hashdatabase import *
from lib.utils.sha256download import download_hashes

class HashUpdater:
    """Fetches daily hash updates from Abuse.ch and merges into local DB."""

    def __init__(self, db: HashDatabase, logger):
        self.db = db
        self.logger = logger

    
    def _read_update(self):
        """Read, parse, and store new SHA256 hashes efficiently from a large file."""
        if os.path.exists(r'lib\utils\.is_dump'):
            return 
        else:
            with open(r'lib\utils\.is_dump',"w")as d:
                d.write("dump")
        try:
            before = self.db.count()
            
            sha256list = download_hashes()
            batch = []
            for line in sha256list:
                h = line.strip()
                if len(h) == 64:  # only valid SHA256
                    batch.append((h,))
                # Insert in batches of 10k to reduce memory usage
                if len(batch) >= 10000:
                    self.db.insert_many([x[0] for x in batch])
                    batch = []
            # Insert remaining hashes
            if batch:
                self.db.insert_many([x[0] for x in batch])

            after = self.db.count()
            added = after - before
            self.logger.info(f"Loaded {added} new hashes into the database.")

        except Exception as e:
            self.logger.warning(f"Failed to read/update hash list: {e}")
    
    def update(self):
        """Download, parse, and store new SHA256 hashes."""
        try:
            self.logger.info("Downloading latest malicious hash list from Abuse.ch...")
            resp = requests.get(HASH_SOURCE_URL, timeout=30)
            if resp.status_code != 200:
                self.logger.warning(f"Failed to fetch hashes. HTTP {resp.status_code}")
                return

            lines = [x.strip() for x in resp.text.splitlines() if len(x.strip()) == 64]
            before = self.db.count()
            self.db.insert_many(lines)
            after = self.db.count()
            added = after - before
            self.logger.info(f"✅ Added {added} new hashes. Total: {after:,}")
        except Exception as e:
            self.logger.warning(f"Failed to update hash list: {e}")
        self._read_update()
