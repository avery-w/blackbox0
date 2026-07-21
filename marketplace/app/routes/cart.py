from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).order_by(CartItem.created_at.desc()).all()
    subtotal = sum(item.subtotal for item in cart_items)
    item_count = sum(item.quantity for item in cart_items)
    return render_template('cart/view.html', cart_items=cart_items, subtotal=subtotal,
                           item_count=item_count, title='Shopping Cart')


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)

    if not product.is_active:
        flash('This product is no longer available.', 'warning')
        return redirect(url_for('products.detail', product_id=product.id))

    if quantity > product.quantity:
        flash(f'Sorry, only {product.quantity} items in stock.', 'warning')
        return redirect(url_for('products.detail', product_id=product.id))

    # Check if product already in cart
    existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if existing:
        new_qty = existing.quantity + quantity
        if new_qty > product.quantity:
            new_qty = product.quantity
        existing.quantity = new_qty
        flash(f'Updated quantity for {product.name} in your cart.', 'info')
    else:
        item = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
        db.session.add(item)
        flash(f'{product.name} added to cart!', 'success')

    db.session.commit()
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    quantity = request.form.get('quantity', 1, type=int)
    if quantity < 1:
        quantity = 1
    if quantity > item.product.quantity:
        quantity = item.product.quantity

    item.quantity = quantity
    db.session.commit()
    flash('Cart updated.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    product_name = item.product.name
    db.session.delete(item)
    db.session.commit()
    flash(f'{product_name} removed from cart.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Cart cleared.', 'info')
    return redirect(url_for('cart.view_cart'))

