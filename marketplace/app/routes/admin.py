from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, Store, Product, Order, OrderItem

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
@login_required
def check_admin():
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('main.home'))


@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    total_users = User.query.count()
    total_stores = Store.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total)).filter(
        Order.status == 'delivered'
    ).scalar() or 0

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    # Orders by status
    pending_orders = Order.query.filter_by(status='pending').count()
    processing_orders = Order.query.filter_by(status='processing').count()
    shipped_orders = Order.query.filter_by(status='shipped').count()
    delivered_orders = Order.query.filter_by(status='delivered').count()
    cancelled_orders = Order.query.filter_by(status='cancelled').count()

    return render_template('admin/dashboard.html',
                           total_users=total_users, total_stores=total_stores,
                           total_products=total_products, total_orders=total_orders,
                           total_revenue=total_revenue, recent_orders=recent_orders,
                           recent_users=recent_users,
                           pending_orders=pending_orders, processing_orders=processing_orders,
                           shipped_orders=shipped_orders, delivered_orders=delivered_orders,
                           cancelled_orders=cancelled_orders,
                           title='Admin Dashboard')


@admin_bp.route('/users')
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users, title='Manage Users')


@admin_bp.route('/user/<int:user_id>/toggle-seller', methods=['POST'])
def toggle_seller(user_id):
    user = User.query.get_or_404(user_id)
    user.is_seller = not user.is_seller
    db.session.commit()
    flash(f'Seller status toggled for {user.username}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/user/<int:user_id>/toggle-admin', methods=['POST'])
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin status toggled for {user.username}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/stores')
def stores():
    page = request.args.get('page', 1, type=int)
    stores = Store.query.order_by(Store.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/stores.html', stores=stores, title='Manage Stores')


@admin_bp.route('/store/<int:store_id>/toggle', methods=['POST'])
def toggle_store(store_id):
    store = Store.query.get_or_404(store_id)
    store.is_active = not store.is_active
    db.session.commit()
    flash(f'Store {"activated" if store.is_active else "deactivated"}.', 'success')
    return redirect(url_for('admin.stores'))


@admin_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/products.html', products=products, title='Manage Products')


@admin_bp.route('/product/<int:product_id>/toggle', methods=['POST'])
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    flash(f'Product {"activated" if product.is_active else "deactivated"}.', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
def orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter, title='Manage Orders')


@admin_bp.route('/order/<int:order_id>/update-status', methods=['POST'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.order_number} status updated to {new_status}.', 'success')
    return redirect(url_for('admin.orders'))

