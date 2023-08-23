from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder


# separator between auth and order
order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


session = Session(bind=engine)


@order_router.post('/order, status_code=status.HTTP_201_CREATED')
async def place_an_order(order: OrderModel, authorize: AuthJWT = Depends()):
    """
    ## placing and order
    This requires the following
    -quantity: integer
    -pizza_size: str

    """



    try:
        authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user = user

    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(authorize: AuthJWT = Depends()):
    """
    ## List all orders
    This lists all orders made: it can be accessed by superusers

    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user)

    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )


@order_router.get('/orders/{id}')
async def get_order_by_id(id:int,authorize: AuthJWT=Depends()):
    """
    ## get an order by it Id
    This gets an order by its Id
    is only accessed by superuser

    """


    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token")

    user=authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to carry out required"
    )


@order_router.get('/user/orders')
async def get_user_orders(authorize:AuthJWT=Depends()):
    """
    ## Get a current user's orders
    this lists the orders made by the currently logged in users
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user=authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first

    return jsonable_encoder(current_user.orders)


@order_router.get('/user/order/{order_id}', response_model=OrderModel)
async def get_specific_order(id:int,authorize:AuthJWT=Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    subject=authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject)

    orders=current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No order with such user")


@order_router.put('/order/update/{order_id}')
async def update_order(id:int, authorize:AuthJWT=Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    order_to_update = session.query(Order).filter(Order.order.id == id).first()

    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size

    session.commit()

    response = {"}id": order_to_update.id,
                "quantity": order_to_update.quantity,
                "pizza_size": order_to_update.pizza_size,
                "order_status": order_to_update.order_status
                }

    return jsonable_encoder(response)


@order_router.patch('/order/update/{id}')
async def update_order_status(id:int,  order: OrderStatusModel, authorize:AuthJWT=Depends()):

    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    username=authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id == id).first()

        order_to_update.order_status=order.order_status

        session.commit()

        response = {"}id": order_to_update.id,
                    "quantity": order_to_update.quantity,
                    "pizza_size": order_to_update.pizza_size,
                    "order_status": order_to_update.order_status
        }

        return jsonable_encoder(response)


@order_router.delete('/order/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int,authorize:AuthJWT=Depends()):

    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")

    order_to_delete=session.query(Order).filter(Order.id==id).first

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete
