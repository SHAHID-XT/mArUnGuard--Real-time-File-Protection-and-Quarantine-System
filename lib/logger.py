from lib.configurations import *

def setup_logger():
    """Initialize mArUnGuard logger."""
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("mArUnGuard")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    fh = logging.FileHandler("logs/mArUnGuard.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger

