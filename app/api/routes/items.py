import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models.Items import Item, ItemPublic, ItemsPublic
from app.requests.ItemRequest import ItemCreate, ItemUpdate
from app.requests.GeneralRequest import Message

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def read_items(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """

    count_statement = (
        select(func.count())
        .select_from(Item)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Item)
        .offset(skip)
        .limit(limit)
    )
    items = session.exec(statement).all()

    res = []
    res.append(count)
    res.append(items)
    return res

@router.post("/")
def create_item(
    *, session: SessionDep, item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    current_user = uuid.UUID("7ad93abe-cf75-4d55-a668-1b7e318a17d2")

    item = Item.model_validate(item_in, update={"owner_id": current_user})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/{id}")
def delete_item(
    session: SessionDep, id: uuid.UUID
) -> Message:
    """
    Delete an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")
