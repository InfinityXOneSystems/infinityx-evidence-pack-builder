import os
from service import EvidencePackBuilder

# Set your Firebase project ID here
# For local testing, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable
# points to your service account key file.
PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "your-firebase-project-id")

def main():
    print(f"Initializing EvidencePackBuilder for project: {PROJECT_ID}")
    builder = EvidencePackBuilder(project_id=PROJECT_ID)

    # 1. Create an Evidence Pack
    print("\nCreating an evidence pack...")
    pack_name = "Incident Report 2026-01-09"
    pack_description = "Evidence collected for a security incident on January 9, 2026."
    created_by = "manus_ai"
    pack_tags = ["security", "incident", "2026"]
    pack_id, pack_data = builder.create_evidence_pack(pack_name, pack_description, created_by, pack_tags)
    print(f"Created Pack ID: {pack_id}")
    print(f"Pack Data: {pack_data}")

    # 2. Add Evidence Items to the Pack
    print("\nAdding evidence items...")
    item1_type = "file"
    item1_description = "Screenshot of compromised system."
    item1_url = "https://storage.googleapis.com/evidence-bucket/incident-2026-01-09/screenshot.png"
    item1_mime_type = "image/png"
    item1_metadata = {"fileHash": "sha256:abcdef1234567890", "fileSize": 123456}
    item1_id, item1_data = builder.add_evidence_item(pack_id, item1_type, item1_description, item1_url, item1_mime_type, created_by, item1_metadata)
    print(f"Added Item 1 ID: {item1_id}")
    print(f"Item 1 Data: {item1_data}")

    item2_type = "log"
    item2_description = "Relevant server logs."
    item2_url = "https://storage.googleapis.com/evidence-bucket/incident-2026-01-09/server.log"
    item2_mime_type = "text/plain"
    item2_metadata = {"logSource": "web_server", "lines": 500}
    item2_id, item2_data = builder.add_evidence_item(pack_id, item2_type, item2_description, item2_url, item2_mime_type, created_by, item2_metadata)
    print(f"Added Item 2 ID: {item2_id}")
    print(f"Item 2 Data: {item2_data}")

    # 3. Get an Evidence Pack
    print("\nRetrieving evidence pack...")
    retrieved_pack_id, retrieved_pack_data = builder.get_evidence_pack(pack_id)
    print(f"Retrieved Pack ID: {retrieved_pack_id}")
    print(f"Retrieved Pack Data: {retrieved_pack_data}")

    # 4. List Evidence Items in a Pack
    print("\nListing evidence items...")
    items = builder.list_evidence_items(pack_id)
    for item_id, item_data in items:
        print(f"  Item ID: {item_id}, Item Data: {item_data}")

    # 5. Update an Evidence Pack
    print("\nUpdating evidence pack status...")
    updated_pack_id, updated_pack_data = builder.update_evidence_pack(pack_id, status="completed")
    print(f"Updated Pack ID: {updated_pack_id}")
    print(f"Updated Pack Data: {updated_pack_data}")

    # 6. Update an Evidence Item
    print("\nUpdating an evidence item description...")
    updated_item1_id, updated_item1_data = builder.update_evidence_item(pack_id, item1_id, description="Updated screenshot description.")
    print(f"Updated Item 1 ID: {updated_item1_id}")
    print(f"Updated Item 1 Data: {updated_item1_data}")

    # 7. Delete an Evidence Item (Optional, uncomment to test)
    # print("\nDeleting an evidence item...")
    # builder.delete_evidence_item(pack_id, item1_id)
    # print(f"Item {item1_id} deleted.")

    # 8. Delete an Evidence Pack (Optional, uncomment to test)
    # print("\nDeleting an evidence pack...")
    # builder.delete_evidence_pack(pack_id)
    # print(f"Pack {pack_id} deleted.")

if __name__ == "__main__":
    main()
