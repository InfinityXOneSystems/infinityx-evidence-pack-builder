import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

class EvidencePackBuilder:
    def __init__(self, project_id=None):
        if not firebase_admin._apps:
            # Initialize Firebase Admin SDK if not already initialized
            # For local development, you might need to set GOOGLE_APPLICATION_CREDENTIALS
            # environment variable to the path of your service account key file.
            # For deployment on Google Cloud, it will automatically pick up credentials.
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id,
            })
        self.db = firestore.client()

    def create_evidence_pack(self, name, description, created_by, tags=None):
        if tags is None:
            tags = []
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        pack_ref = self.db.collection('evidencePacks').document()
        pack_data = {
            'name': name,
            'description': description,
            'createdAt': timestamp,
            'updatedAt': timestamp,
            'status': 'draft',
            'createdBy': created_by,
            'tags': tags
        }
        pack_ref.set(pack_data)
        return pack_ref.id, pack_data

    def get_evidence_pack(self, pack_id):
        pack_ref = self.db.collection('evidencePacks').document(pack_id)
        pack = pack_ref.get()
        if pack.exists:
            return pack.id, pack.to_dict()
        return None

    def update_evidence_pack(self, pack_id, **kwargs):
        pack_ref = self.db.collection('evidencePacks').document(pack_id)
        kwargs['updatedAt'] = datetime.datetime.now(datetime.timezone.utc)
        pack_ref.update(kwargs)
        return self.get_evidence_pack(pack_id)

    def delete_evidence_pack(self, pack_id):
        pack_ref = self.db.collection('evidencePacks').document(pack_id)
        pack_ref.delete()
        return True

    def add_evidence_item(self, pack_id, item_type, description, url, mime_type, created_by, metadata=None):
        if metadata is None:
            metadata = {}
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        item_ref = self.db.collection('evidencePacks').document(pack_id).collection('evidenceItems').document()
        item_data = {
            'packId': pack_id,
            'type': item_type,
            'description': description,
            'url': url,
            'mimeType': mime_type,
            'createdAt': timestamp,
            'createdBy': created_by,
            'metadata': metadata
        }
        item_ref.set(item_data)
        self.update_evidence_pack(pack_id, updatedAt=timestamp) # Update parent pack's updatedAt
        return item_ref.id, item_data

    def get_evidence_item(self, pack_id, item_id):
        item_ref = self.db.collection('evidencePacks').document(pack_id).collection('evidenceItems').document(item_id)
        item = item_ref.get()
        if item.exists:
            return item.id, item.to_dict()
        return None

    def update_evidence_item(self, pack_id, item_id, **kwargs):
        item_ref = self.db.collection('evidencePacks').document(pack_id).collection('evidenceItems').document(item_id)
        item_ref.update(kwargs)
        self.update_evidence_pack(pack_id, updatedAt=datetime.datetime.now(datetime.timezone.utc)) # Update parent pack's updatedAt
        return self.get_evidence_item(pack_id, item_id)

    def delete_evidence_item(self, pack_id, item_id):
        item_ref = self.db.collection('evidencePacks').document(pack_id).collection('evidenceItems').document(item_id)
        item_ref.delete()
        self.update_evidence_pack(pack_id, updatedAt=datetime.datetime.now(datetime.timezone.utc)) # Update parent pack's updatedAt
        return True

    def list_evidence_items(self, pack_id):
        items_ref = self.db.collection('evidencePacks').document(pack_id).collection('evidenceItems')
        items = items_ref.stream()
        return [(item.id, item.to_dict()) for item in items]

if __name__ == '__main__':
    # This is a placeholder for testing. In a real scenario, you would configure
    # your Firebase project ID and potentially service account credentials.
    # For local testing, ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    # Example usage:
    # builder = EvidencePackBuilder(project_id='your-firebase-project-id')
    # pack_id, pack_data = builder.create_evidence_pack('Test Pack', 'A pack for testing', 'test_user', ['test'])
    # print(f'Created pack: {pack_id}, {pack_data}')
    # item_id, item_data = builder.add_evidence_item(pack_id, 'file', 'Test File', 'http://example.com/test.txt', 'text/plain', 'test_user')
    # print(f'Added item: {item_id}, {item_data}')
    pass
