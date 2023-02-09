from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .entry_schema import CreateEntry, EntryOut
from .entries_model import Entry
from ..db.database import get_db
from ..utils.oauth2 import get_current_user


router = APIRouter()


@router.get("/entries", response_model=List[EntryOut])
def get_entries(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = "",
):

    entries = (
        db.query(Entry)
        .filter(
            Entry.owner_id == current_user.id,
            or_(
                Entry.title.ilike(f"%{search}%"),
                Entry.content.ilike(f"%{search}%"),
            ),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    if entries == []:
        raise HTTPException(
            status_code=404,
            detail=f"No dairy entries found... Create new entry",
        )
    return entries


@router.get("/entries/{id}", response_model=EntryOut)
def get_entry_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    entry = db.query(Entry).filter(Entry.id == id).first()
    if not entry:
        raise HTTPException(
            status_code=404, detail=f"Entry with id {id} not found"
        )
    if entry.owner_id != current_user.id:
        raise HTTPException(
            status_code=401, detail=f"Unauthorized to get entry with id {id}"
        )
    return entry


@router.post("/entries", response_model=EntryOut, status_code=201)
def create_entry(
    entry: CreateEntry,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_entry = Entry(**entry.dict(), owner_id=current_user.id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry
