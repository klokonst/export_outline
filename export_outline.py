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

def resolve_ids(doc_id):
    res_doc = requests.post(f"{config.BASE_URL}/documents.info", headers=HEADERS, json={"id": doc_id})
    if res_doc.status_code != 200:
        print(f"Error: Document {doc_id} not found.")
        return None, None
    
    doc_data = res_doc.json().get('data', {})
    return doc_data.get('collectionId'), doc_data.get('id'), doc_data.get('title')

def build_tree(documents):
    nodes = {doc['id']: {**doc, 'children': []} for doc in documents}
    tree = []
    for node in nodes.values():
        parent_id = node.get('parentDocumentId')
        if parent_id and parent_id in nodes:
            nodes[parent_id]['children'].append(node)
        else:
            tree.append(node)
    return tree

def find_target_node(nodes, target_id):
    for node in nodes:
        if node.get('id') == target_id:
            return node
        if node.get('children'):
            found = find_target_node(node['children'], target_id)
            if found:
                return found
    return None

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
    coll_uuid, doc_uuid, doc_title = resolve_ids(config.TARGET_DOCUMENT_ID)
    if not coll_uuid or not doc_uuid:
        return

    print(f"Target: {doc_title}")
    
    res = requests.post(
        f"{config.BASE_URL}/documents.list", 
        headers=HEADERS, 
        json={"collectionId": coll_uuid, "limit": 100}
    )
    
    if res.status_code != 200:
        print(f"API Error: {res.text}")
        return
        
    documents = res.json().get('data', [])
    tree = build_tree(documents)
    target_node = find_target_node(tree, doc_uuid)
    
    if not target_node:
        print("Error: Document not found in tree.")
        return
        
    docs_to_download = build_export_list(target_node)
    print(f"Downloading {len(docs_to_download)} documents...\n")
    
    for doc in docs_to_download:
        file_path = os.path.join(config.OUTPUT_DIR, f"{doc['path']}.md")
        download_document(doc['id'], file_path)
        time.sleep(0.3) 

    print(f"\nDone! Exported to: {config.OUTPUT_DIR}")

if __name__ == "__main__":
    main()
