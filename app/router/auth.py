from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.models.user import User
from app.core.db import SessionDep
from sqlmodel import select
from app.core.segurity import hash_password, verify_password

router = APIRouter(prefix="/auth")

@router.post('/register', response_model=UserRead, tags=["auth"])
async def register(user_data: UserCreate, session: SessionDep):
    
    # Verificar si el email ya existe
    email = session.exec(select(User).where(User.email == user_data.email)).first()
    if email:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Verificar si el username ya existe
    username = session.exec(select(User).where(User.username == user_data.username)).first()
    if username:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    # Crear el nuevo usuario
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=user_data.role
    )

    # Agregar a la sesión y commit
    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Para obtener el id generado

    # Retornar el usuario sin la contraseña
    return UserRead(id=new_user.id, username=new_user.username, email=new_user.email, role=new_user.role)

@router.post('/login', response_model=UserRead, tags=["auth"])
async def login(data: UserLogin, session: SessionDep):
    # Buscar el usuario por email
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Verificar la contraseña
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return UserRead(id=user.id, username=user.username, email=user.email, role=user.role)