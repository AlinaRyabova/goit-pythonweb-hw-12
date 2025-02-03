from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.users import UserCreate, Token, User
from src.services.auth import create_access_token, Hash, get_email_from_token
from src.services.users import UserService
from src.database.db import get_db
from src.schemas.users import RequestEmail
from fastapi import BackgroundTasks, Request
from src.services.email import send_email


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Реєстрація нового користувача в системі.

    Перевіряє, чи не існує користувач з таким самим email або ім'ям, хешує пароль,
    створює нового користувача в базі даних та надсилає електронний лист для підтвердження.

    Args:
        user_data (UserCreate): Дані користувача для реєстрації.
        background_tasks (BackgroundTasks): Фонові завдання для надсилання електронного листа.
        request (Request): Запит, використовується для отримання базового URL.
        db (Session): Сесія бази даних.

    Returns:
        User: Створений користувач.
    """
    user_service = UserService(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким email вже існує",
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким іменем вже існує",
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url
    )
    return new_user

@router.post("/login", response_model=Token)
async def login_user(
     form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Логін користувача в систему та отримання токену доступу.

    Перевіряє, чи існує користувач, чи підтверджена електронна адреса, та чи правильно введений пароль.
    Якщо все вірно, створює токен доступу.

    Args:
        form_data (OAuth2PasswordRequestForm): Дані форми для входу користувача.
        db (Session): Сесія бази даних.

    Returns:
        dict: Токен доступу.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Електронна адреса не підтверджена",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Підтвердження електронної пошти за допомогою токену.

    Перевіряє, чи користувач існує та чи підтверджена його електронна пошта. Якщо ні, підтверджує.

    Args:
        token (str): Токен підтвердження електронної пошти.
        db (Session): Сесія бази даних.

    Returns:
        dict: Повідомлення про статус підтвердження.
    """
    email = await get_email_from_token(token)
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Ваша електронна пошта вже підтверджена"}
    await user_service.confirmed_email(email)
    return {"message": "Електронну пошту підтверджено"}

@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Запит на відправку електронного листа для підтвердження електронної пошти користувача.

    Перевіряє, чи користувач існує та чи підтверджена його пошта. Якщо не підтверджена, надсилає лист.

    Args:
        body (RequestEmail): Дані користувача для підтвердження.
        background_tasks (BackgroundTasks): Фонові завдання для надсилання електронного листа.
        request (Request): Запит, використовується для отримання базового URL.
        db (Session): Сесія бази даних.

    Returns:
        dict: Повідомлення про запит на підтвердження електронної пошти.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)

    if user.confirmed:
        return {"message": "Ваша електронна пошта вже підтверджена"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url
        )
    return {"message": "Перевірте свою електронну пошту для підтвердження"}


