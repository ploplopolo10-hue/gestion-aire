from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Project, Task, User
from ..schemas import ProjectCreate, ProjectOut, TaskCreate, TaskOut

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Project).where(Project.owner_id == user.id).order_by(Project.created_at.desc())).all()

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.status not in {"active", "paused", "completed"}:
        raise HTTPException(status_code=422, detail="Invalid project status")
    project = Project(**payload.model_dump(), owner_id=user.id)
    db.add(project); db.commit(); db.refresh(project)
    return project

@router.get("/{project_id}/tasks", response_model=list[TaskOut])
def list_tasks(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.owner_id == user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.scalars(select(Task).where(Task.project_id == project_id).order_by(Task.created_at.desc())).all()

@router.post("/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, payload: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.owner_id == user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.status not in {"todo", "in_progress", "done"}:
        raise HTTPException(status_code=422, detail="Invalid task status")
    if payload.priority not in {"low", "normal", "high"}:
        raise HTTPException(status_code=422, detail="Invalid task priority")
    task = Task(**payload.model_dump(), project_id=project.id)
    db.add(task); db.commit(); db.refresh(task)
    return task
