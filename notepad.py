import os
import json
import uuid
from datetime import datetime
from typing import Optional


class NotePad:

    def __init__(self):
        base_path = os.path.dirname(__file__)
        self.dir_path = os.path.join(base_path, "notes")
        self.attachments_path = os.path.join(self.dir_path, "attachments")

        os.makedirs(self.dir_path, exist_ok=True)
        os.makedirs(self.attachments_path, exist_ok=True)

        self.categories = ["work", "personal", "study", "other"]


    def create_note(self, title: str, content: str, category: Optional[str] = None):

        note_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        note_data = {
            "id": note_id,
            "title": title,
            "content": content,
            "category": category,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        file_path = os.path.join(self.dir_path, f"{note_id}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(note_data, f, indent=2, ensure_ascii=False)

        return note_data


    def get_notes(self, category: Optional[str] = None):

        notes = []

        for file in os.listdir(self.dir_path):
            if not file.endswith(".json"):
                continue

            with open(os.path.join(self.dir_path, file), "r", encoding="utf-8") as f:
                note = json.load(f)

                if category is None or note.get("category") == category:
                    notes.append(note)

        notes.sort(key=lambda x: x["created_at"], reverse=True)

        return {
            "total_notes": len(notes),
            "last_5": notes[:5],
            "categories": self.categories
        }