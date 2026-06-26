import os
import re
import time
import requests
import config

HEADERS = {
    "Authorization": f"Bearer {config.API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def sanitize_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def fetch_document_tree(doc_id):
    res = requests.post(
        f"{config.BASE_URL}/documents.documents",
        headers=HEADERS,
        json={"id": doc_id},
    )
    if res.status_code != 200:
        print(f"API Error: {res.text}")
        return None
    return res.json().get("data")

def build_export_list(node, current_path=""):
    export_list = []
    title = sanitize_name(node.get('title', 'Untitled'))
    node_path = os.path.join(current_path, title) if current_path else title
    
    export_list.append({"id": node.get('id'), "title": title, "path": node_path})
    
    for child in node.get('children', []):
        export_list.extend(build_export_list(child, node_path))
        
    return export_list

def download_document(doc_id, save_path):
    url = f"{config.BASE_URL}/documents.info"
    response = requests.post(url, headers=HEADERS, json={"id": doc_id})
    
    if response.status_code == 200:
        text = response.json().get('data', {}).get('text', '')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: {save_path}")
    else:
        print(f"Error downloading {doc_id}: {response.status_code}")

def main():
    target_node = fetch_document_tree(config.TARGET_DOCUMENT_ID)
    if not target_node:
        return

    print(f"Target: {target_node.get('title', 'Untitled')}")

    docs_to_download = build_export_list(target_node)
    print(f"Downloading {len(docs_to_download)} documents...\n")
    
    for doc in docs_to_download:
        file_path = os.path.join(config.OUTPUT_DIR, f"{doc['path']}.md")
        download_document(doc['id'], file_path)
        time.sleep(0.3) 

    print(f"\nDone! Exported to: {config.OUTPUT_DIR}")

if __name__ == "__main__":
    main()
