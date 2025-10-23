
from ..configurations import *
from ..logger import *
from lib.utils.notifier import *

class FileWatcher(FileSystemEventHandler):
    """Monitors filesystem events and handles scanning."""

    def __init__(self, db: HashDatabase, quarantine: QuarantineManager, notifier: Notifier, logger):
        super().__init__()
        self.db = db
        self.quarantine = quarantine
        self.notifier = notifier
        self.logger = logger

    @staticmethod
    def compute_sha256(path):
        """Compute SHA256 for a file."""
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    
    
    def _should_scan(self,path):
        path = Path(path).resolve()
        for ignored in IGNORED_PATHS:
            ignored_path = Path(ignored).resolve()
            if str(path).startswith(str(ignored_path)):
                return True
        return 
    
    
    def process(self, path):
        """Process new or modified files."""
        
        if self._should_scan(path):
            return
        
        _, extension = os.path.splitext(path) # spliting with filename and file extension
        
        if extension: # checking if empty extension
            if not path.endswith(HIGH_RISK_EXTENSIONS): #continue only if high risk extension found else return None
                return None
        try:
            if not os.path.isfile(path) or os.path.getsize(path) == 0:
                return
            sha256 = self.compute_sha256(path)
            if self.db.exists(sha256):
                self.logger.warning(f"⚠️ Malicious file detected: {path}")
                self.quarantine.quarantine(path)
                self.notifier.vt_url = f"https://www.virustotal.com/gui/file/{sha256}"
                self.vt_url = f"https://www.virustotal.com/gui/file/{sha256}"
                self.notifier.notify("⚠️ Malware Detected!",
                                f"The file '{os.path.basename(path)}' has been identified as malicious and quarantined for your safety.\n"
                                f"Click here to view a detailed VirusTotal analysis of this file.",
                                found_malware=True
                            )
            else:
                self.logger.info(f"Scanned safe file: {path}")
        except Exception as e:
            pass
    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process(event.src_path)

