from ..configurations import *
from ..logger import *
from lib.utils.hashupdater import *

class QuarantineManager:
    """Moves and locks malicious files."""

    def __init__(self, quarantine_dir=QUARANTINE_PATH, logger=None):
        self.logger = logger
        self.quarantine_dir = Path(quarantine_dir)
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def quarantine(self, file_path):
        """Move file to quarantine safely and restrict access."""
        try:
            file_path = Path(file_path) 
            if not os.path.isfile(file_path):
                return
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # Rename file with .mr extension
            target = self.quarantine_dir / f"{file_path.stem}_{timestamp}.mr"
            shutil.move(str(file_path), str(target))
            # Remove inheritance
            os.system(f'icacls "{target}" /inheritance:r /deny Everyone:(R)')
            os.system(f'icacls "{target}" /deny Everyone:F')
            self.logger.info(f"Quarantined file with restricted permissions: {target}")
        except Exception as e:
            self.logger.warning(f"Failed to quarantine {file_path}: {e}")
