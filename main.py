
from lib.utils.filewatcher import *
class mArUnGuard:
    """Core system orchestrator for mArUnGuard."""

    
    def __init__(self):
        self.logger = setup_logger()
        self.db = HashDatabase(DB_FILE)
        self.notifier = Notifier()
        self.quarantine = QuarantineManager(logger=self.logger)
        self.watcher = FileWatcher(self.db, self.quarantine, self.notifier, self.logger)
        self.observer = Observer()
        self.updater = HashUpdater(self.db, self.logger)
        self.paths = WATCH_PATHS

    def start(self):
        """Start monitoring and initialize components."""
        self.logger.info("🚀 Starting mArUnGuard by Shahid-Xt")
        self.logger.info("Initializing hash database and fetching updates...")

        # Update hash list on startup
        self.updater.update()

        total = self.db.count()
        self.logger.info(f"Loaded {total:,} SHA256 hashes into local database.")

        for path in self.paths:
            if os.path.exists(path):
                self.logger.info(f"📂 Watching: {path}")
                self.observer.schedule(self.watcher, path, recursive=True)
            else:
                self.logger.warning(f"⚠️ Path not found: {path}")

        self.observer.start()
        self.notifier.notify("🛡️ mArUnGuard Active",
                             "Your system is now being monitored for malicious files.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Graceful shutdown."""
        self.logger.info("🛑 Stopping mArUnGuard...")
        self.observer.stop()
        self.observer.join()
        now = datetime.now(timezone.utc).isoformat()
        self.logger.info(f"Shutdown completed at {now}")
        self.notifier.notify("🛑 mArUnGuard Stopped", "Protection has been disabled.")

    def is_admin(self):
        """Check if the script is running as admin."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def is_running_as_admin(self):
        """Relaunch the script as admin if not already."""
        if not self.is_admin():
            print("⚠️ Insufficient privileges. Attempting to run as administrator...")
            # Build command: python <script> <args>
            script = os.path.abspath(sys.argv[0])
            params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
            cmd = f'"{sys.executable}" "{script}" {params}'

            # Request elevation
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1
            )
            sys.exit()

if __name__ == "__main__":
    guard = mArUnGuard()
    guard.is_running_as_admin()
    guard.start()
