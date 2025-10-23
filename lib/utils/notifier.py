from ..configurations import *
from ..logger import *
from lib.utils.quarantinemanager import *


class Notifier:
    """Handles Windows toast notifications."""
    vt_url = "test"
    def __init__(self, icon=r"Assets\icon.ico"):
        self.icon = icon if os.path.exists(icon) else ''
        self.toast = ToastNotifier()
        
    def on_click(self):
            try:
                webbrowser.open(self.vt_url)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to open VirusTotal page: {e}")
    def notify(self, title, message, duration=6,found_malware=False):
        """Show toast message."""
        try:
            if found_malware:
                self.toast.show_toast(
                        title,
                        message,
                        icon_path=self.icon,
                        duration=duration,
                        threaded=True,
                        callback_on_click=self.on_click
                    )
                
            self.toast.show_toast(
                    title,
                    message,
                    icon_path=self.icon,
                    duration=duration,
                    threaded=True,
                )
        except Exception as e:
            pass

