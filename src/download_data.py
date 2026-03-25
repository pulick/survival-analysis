import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os

GDC_API = "https://api.gdc.cancer.gov"
SAVE_DIR = "C:/Users/abrup/Desktop/Project/survival-analysis/data/raw/genomic"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- 1. Setup a Robust Session ---
def get_robust_session():
    session = requests.Session()
    # Retry 5 times on connection errors or specific server status codes
    retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

# --- 2. Keep your existing filters ---
filters = {
    "op": "and",
    "content": [
        {"op": "=", "content": {"field": "cases.project.project_id", "value": "TCGA-BRCA"}},
        {"op": "=", "content": {"field": "files.data_category", "value": "Transcriptome Profiling"}},
        {"op": "=", "content": {"field": "files.data_type", "value": "Gene Expression Quantification"}}
    ]
}

params = {
    "filters": json.dumps(filters),
    "fields": "file_id,file_name",
    "format": "JSON",
    "size": "20"
}

session = get_robust_session()

print("🔎 Searching files...")
response = session.get(f"{GDC_API}/files", params=params)
files = response.json()["data"]["hits"]
print(f"Files found: {len(files)}")

# --- 3. Optimized Download Loop ---
for file in files:
    file_id = file["file_id"]
    file_name = file["file_name"]
    filepath = os.path.join(SAVE_DIR, file_name)

    # Skip if file already exists
    if os.path.exists(filepath):
        print(f"⏩ Skipping (already exists): {file_name}")
        continue

    print(f"⬇ Downloading: {file_name}")
    
    try:
        # Added 'timeout' to prevent the script from hanging forever
        r = session.get(f"{GDC_API}/data/{file_id}", stream=True, timeout=60)
        r.raise_for_status()
        
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size) * 100 if total_size else 0
                    print(f"\r   Progress: {percent:.1f}%", end="")
        print(f"\n✅ Finished: {file_name}")

    except Exception as e:
        print(f"\n❌ Error downloading {file_name}: {e}")
        # Optionally delete the partial file so it doesn't count as "exists" next time
        if os.path.exists(filepath):
            os.remove(filepath)

print("\n🎯 Download process complete!")