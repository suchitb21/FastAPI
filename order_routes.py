from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User,Order
from schemas import OrderModel
from database import get_db
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

order_router=APIRouter(
    prefix='/orders',
    tags=['orders']
)

# session=Session(bind=engine)

@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"

        )
    return{"message":"Hello World"}


@order_router.post('/order',status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel,Authorize:AuthJWT=Depends(), db : Session = Depends(get_db)):



    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"

        )
    
    current_user=Authorize.get_jwt_subject()

    user=db.query(User).filter(User.username==current_user).first()


    new_order=Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user=user

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    response={
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status,
        "user_id":new_order.user_id,
        "username":new_order.user.username
    }

    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends(), db : Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'                    
        )
    
    current_user=Authorize.get_jwt_subject()
    
    user=db.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders=db.query(Order).all()

        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not a superuser'                    
        )


