"""Main script for the infinityx-evidence-pack-builder.
"""
import os
from service import EvidencePackBuilder

PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "your-firebase-project-id")

def _create_evidence_pack(builder):
    """Creates an evidence pack and returns its ID."""
    print("\nCreating an evidence pack...")
    pack_name = "Incident Report 2026-01-09"
    pack_description = (
        "Evidence collected for a security incident on January 9, 2026."
    )
    created_by = "manus_ai"
    pack_tags = ["security", "incident", "2026"]
    pack_id, pack_data = builder.create_evidence_pack(
        pack_name, pack_description, created_by, pack_tags
    )
    print(f"Created Pack ID: {pack_id}")
    print(f"Pack Data: {pack_data}")
    return pack_id

def _add_evidence_items(builder, pack_id):
    """Adds evidence items to the specified pack and returns their IDs."""
    print("\nAdding evidence items...")
    item1_data = {
        "type": "file",
        "description": "Screenshot of compromised system.",
        "url": "https://storage.googleapis.com/evidence-bucket/incident-2026-01-09/screenshot.png",
        "mimeType": "image/png",
        "createdBy": "manus_ai",
        "metadata": {"fileHash": "sha256:abcdef1234567890", "fileSize": 123456},
    }
    item1_id, item1_data_returned = builder.add_evidence_item(pack_id, item1_data)
    print(f"Added Item 1 ID: {item1_id}")
    print(f"Item 1 Data: {item1_data_returned}")

    item2_data = {
        "type": "log",
        "description": "Relevant server logs.",
        "url": "https://storage.googleapis.com/evidence-bucket/incident-2026-01-09/server.log",
        "mimeType": "text/plain",
        "createdBy": "manus_ai",
        "metadata": {"logSource": "web_server", "lines": 500},
    }
    item2_id, item2_data_returned = builder.add_evidence_item(pack_id, item2_data)
    print(f"Added Item 2 ID: {item2_id}")
    print(f"Item 2 Data: {item2_data_returned}")
    return item1_id, item2_id

def _retrieve_and_list_evidence(builder, pack_id):
    """Retrieves and lists evidence packs and items."""
    print("\nRetrieving evidence pack...")
    retrieved_pack_id, retrieved_pack_data = builder.get_evidence_pack(pack_id)
    print(f"Retrieved Pack ID: {retrieved_pack_id}")
    print(f"Retrieved Pack Data: {retrieved_pack_data}")

    print("\nListing evidence items...")
    items = builder.list_evidence_items(pack_id)
    for item_id, item_data in items:
        print(f"  Item ID: {item_id}, Item Data: {item_data}")

def _update_evidence(builder, pack_id, item1_id):
    """Updates an evidence pack and an evidence item."""
    print("\nUpdating evidence pack status...")
    updated_pack_id, updated_pack_data = builder.update_evidence_pack(
        pack_id, status="completed"
    )
    print(f"Updated Pack ID: {updated_pack_id}")
    print(f"Updated Pack Data: {updated_pack_data}")

    print("\nUpdating an evidence item description...")
    updated_item1_id, updated_item1_data = builder.update_evidence_item(
        pack_id, item1_id, description="Updated screenshot description."
    )
    print(f"Updated Item 1 ID: {updated_item1_id}")
    print(f"Updated Item 1 Data: {updated_item1_data}")

def main():
    """Main function to run the evidence pack builder operations."""
    print(f"Initializing EvidencePackBuilder for project: {PROJECT_ID}")
    builder = EvidencePackBuilder(project_id=PROJECT_ID)

    pack_id = _create_evidence_pack(builder)
    item1_id, _ = _add_evidence_items(builder, pack_id)
    _retrieve_and_list_evidence(builder, pack_id)
    _update_evidence(builder, pack_id, item1_id)

    # Optional: Uncomment to test delete operations
    # print("\nDeleting an evidence item...")
    # builder.delete_evidence_item(pack_id, item1_id)
    # print(f"Item {item1_id} deleted.")

    # print("\nDeleting an evidence pack...")
    # builder.delete_evidence_pack(pack_id)
    # print(f"Pack {pack_id} deleted.")


if __name__ == "__main__":
    main()
