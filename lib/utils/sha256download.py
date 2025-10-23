import requests
import zipfile
import io


def download_hashes():
    url = "https://bazaar.abuse.ch/export/txt/sha256/full/"

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    # Step 2: open it in memory (no need to save to disk)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        # list files inside zip
        txt_files = [name for name in z.namelist() if name.endswith(".txt")]
        with z.open(txt_files[0]) as f:
            content = f.read().decode("utf-8", errors="ignore")

    sha256_list = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    return sha256_list
