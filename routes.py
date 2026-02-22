from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import os
import shutil

from notepad import NotePad


router = APIRouter()
note_pad = NotePad()


def check_category(category: str):

    if category not in note_pad.categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Available: {note_pad.categories}"
        )

    return True



@router.post("/add-note/")
async def add_note(
    title: str,
    content: str,
    category: str,
    file: Optional[UploadFile] = File(None)
):

    check_category(category)

    new_note = note_pad.create_note(title, content, category)

    if file:
        extension = os.path.splitext(file.filename)[1]
        file_name = f"{new_note['id']}{extension}"
        file_path = os.path.join(note_pad.attachments_path, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_note["file"] = file_name

    return {
        "message": "Note successfully added",
        "note": new_note
    }



@router.get("/notes/")
def get_notes(category: Optional[str] = None):

    if category:
        check_category(category)

    result = note_pad.get_notes(category)

    indexed = list(enumerate(result["last_5"]))

    return {
        "statistics": result,
        "indexed_last_5": [
            {
                "order": i + 1,
                "title": note["title"]
            }
            for i, note in indexed
        ]
    }



@router.get("/categories/")
def get_categories():

    category_list = [
        {
            "code": c,
            "description": c
        }
        for c in note_pad.categories
    ]

    return {
        "categories": category_list,
        "total": len(category_list)
    }