from flask import request, jsonify, flash
from . import api
from ..models import Cart, Product, User, db
from ..apiauthhelper import token_auth_required, basic_auth_required, basic_auth

# like and unlike post routes: One uses a built in decorator and one of our custom decorators for contrast!


@api.get('/products')
def get_all_products_API():
    products = Product.query.all()

    return {
        'status': 'ok',
        'results': len(products),
        'products': [p.to_dict() for p in products]
    }, 200

@api.post('/cart/add')
@token_auth_required
def add_to_cart_API(user):
    data = request.json
    product_id = data.get('product_id')
    product = Product.query.get(product_id)

    if product:
        cart_item = Cart(user.id, product.id)
        db.session.add(cart_item)
        db.session.commit()

        return {
            'status': 'ok',
            'message': 'Product added successfully to cart',
        }, 200
    
    else:
        return {
            'status': 'not ok',
            'message': 'Product with that ID does not exist',
        }, 404



@api.post('/cart/remove')
@token_auth_required
def remove_from_cart_API(user):
    data = request.json
    product_id = data.get('product_id')

    cart_item = Cart.query.filter_by(user_id=user.id).filter_by(product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

        return {
            'status': 'ok',
            'message': 'Product removed successfully from cart',
        }, 200

    else:
        return {
            'status': 'not ok',
            'message': 'Product with that ID does not exist in your cart',
        }, 404


@api.get('/cart')
@token_auth_required
def get_cart_API(user):
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart = [Product.query.get(item.product_id).to_dict() for item in cart]

    return {
        'status': 'ok',
        'cart': cart
    }, 200