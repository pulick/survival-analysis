import requests
import json
import os

GDC_API = "https://api.gdc.cancer.gov"
SAVE_DIR = "C:/Users/abrup/Desktop/Project/survival-analysis/data/raw/genomic"

os.makedirs(SAVE_DIR, exist_ok=True)

# -----------------------------
# Correct filters (WORKING)
# -----------------------------
filters = {
    "op": "and",
    "content": [
        {
            "op": "=",
            "content": {
                "field": "cases.project.project_id",
                "value": "TCGA-BRCA"
            }
        },
        {
            "op": "=",
            "content": {
                "field": "files.data_category",
                "value": "Transcriptome Profiling"
            }
        },
        {
            "op": "=",
            "content": {
                "field": "files.data_type",
                "value": "Gene Expression Quantification"
            }
        }
    ]
}

params = {
    "filters": json.dumps(filters),
    "fields": "file_id,file_name",
    "format": "JSON",
    "size": "20"   # small test download
}

print("🔎 Searching files...")

response = requests.get(GDC_API + "/files", params=params)
data = response.json()

files = data["data"]["hits"]

print("Files found:", len(files))

# -----------------------------
# Download files
# -----------------------------
for file in files:
    file_id = file["file_id"]
    file_name = file["file_name"]

    print("⬇ Downloading:", file_name)

    download_url = f"{GDC_API}/data/{file_id}"
    r = requests.get(download_url, stream=True)

total_size = int(r.headers.get('content-length', 0))
downloaded = 0

filepath = os.path.join(SAVE_DIR, file_name)

with open(filepath, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
        if chunk:
            f.write(chunk)
            downloaded += len(chunk)

            percent = (downloaded / total_size) * 100 if total_size else 0
            print(f"\r   Progress: {percent:.1f}%", end="")
print("\n✅ Finished:", file_name)

print("✅ Download complete!")