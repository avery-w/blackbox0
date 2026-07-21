from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, CartItem, Product
from app.forms import CheckoutForm
from app.utils import generate_order_number

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart.view_cart'))

    # Check stock for all items
    for item in cart_items:
        if item.quantity > item.product.quantity:
            flash(f'{item.product.name} only has {item.product.quantity} in stock. Please adjust your cart.', 'warning')
            return redirect(url_for('cart.view_cart'))

    subtotal = sum(item.subtotal for item in cart_items)
    shipping_cost = 0.0 if subtotal >= 50 else 9.99
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + shipping_cost + tax, 2)

    form = CheckoutForm()
    # Pre-fill user info
    if current_user.address:
        form.shipping_address.data = current_user.address
    if current_user.phone:
        form.phone.data = current_user.phone

    if form.validate_on_submit():
        order_number = generate_order_number()

        order = Order(
            order_number=order_number,
            user_id=current_user.id,
            status='pending',
            shipping_address=form.shipping_address.data,
            phone=form.phone.data,
            payment_method=form.payment_method.data,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total=total,
            notes=form.notes.data
        )
        db.session.add(order)
        db.session.flush()

        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                store_id=cart_item.product.store_id,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal
            )
            db.session.add(order_item)

            # Decrease product stock
            cart_item.product.quantity -= cart_item.quantity

        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash(f'Order placed successfully! Order number: {order_number}', 'success')
        return redirect(url_for('orders.order_confirmation', order_id=order.id))

    return render_template('orders/checkout.html', form=form, cart_items=cart_items,
                           subtotal=subtotal, shipping_cost=shipping_cost, tax=tax, total=total,
                           title='Checkout')


@orders_bp.route('/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('orders/confirmation.html', order=order, title='Order Confirmation')


@orders_bp.route('/')
@login_required
def my_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('orders/my_orders.html', orders=orders, title='My Orders')


@orders_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('orders/detail.html', order=order, title=f'Order #{order.order_number}')


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))

    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        # Restore stock
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.quantity += item.quantity
        db.session.commit()
        flash('Order cancelled successfully.', 'success')
    else:
        flash('This order cannot be cancelled.', 'warning')

    return redirect(url_for('orders.order_detail', order_id=order.id))

