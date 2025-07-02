from fastapi import APIRouter,status , Depends
from database import get_db 
from schemas import SignUpModel,LoginModel , UserPublic
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid token"
        )
    return{"message":"Hello World"}

@auth_router.post("/signup",response_model=UserPublic,status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpModel , db: Session = Depends(get_db)):
    
    db_email=db.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the email already exists"            
                             )
    
    
    db_username=db.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the username already exists"            
                             )
    

    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )



    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        
        return UserPublic.from_orm(new_user)


    except Exception as e:
        db.rollback()

        print(f"error during user signup: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="server error")
    
@auth_router.post('/login',status_code=200 )
async def login(user:LoginModel,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password , user.password ):
        access_token=Authorize.create_access_token(subject=db_user.username) 
        refresh_token=Authorize.create_refresh_token(subject=db_user.username)

        response = {
            "access":access_token,
            "refresh":refresh_token
        }
        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
          detail="Invalid username or Password"
    )

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="PLease provide a valid refresh token"                     
        )
    
    current_user=Authorize.get_jwt_subject()

    access_token=Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"acess":access_token})