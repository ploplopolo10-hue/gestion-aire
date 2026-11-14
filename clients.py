from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Client, User
from ..schemas import ClientCreate, ClientOut

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Client).where(Client.owner_id == user.id).order_by(Client.name)).all()

@router.post("", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    client = Client(**payload.model_dump(), owner_id=user.id)
    db.add(client); db.commit(); db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    client = db.scalar(select(Client).where(Client.id == client_id, Client.owner_id == user.id))
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client); db.commit()
