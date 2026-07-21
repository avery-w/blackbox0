import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Store, Product, Order, OrderItem
from app.forms import StoreForm, ProductForm
from app.utils import save_picture

seller_bp = Blueprint('seller', __name__, url_prefix='/seller')


@seller_bp.before_request
@login_required
def check_seller():
    if not current_user.is_seller:
        flash('You need to be a seller to access this page.', 'warning')
        return redirect(url_for('main.home'))


@seller_bp.route('/')
@seller_bp.route('/dashboard')
def dashboard():
    stores = Store.query.filter_by(owner_id=current_user.id).all()
    total_products = sum(s.total_products for s in stores)
    total_sales = sum(s.total_sales for s in stores)
    recent_orders = OrderItem.query.filter(
        OrderItem.store_id.in_([s.id for s in stores])
    ).order_by(OrderItem.id.desc()).limit(10).all() if stores else []

    return render_template('seller/dashboard.html', stores=stores, total_products=total_products,
                           total_sales=total_sales, recent_orders=recent_orders, title='Seller Dashboard')


@seller_bp.route('/store/create', methods=['GET', 'POST'])
def create_store():
    form = StoreForm()
    if form.validate_on_submit():
        store = Store(
            name=form.name.data,
            description=form.description.data,
            owner_id=current_user.id
        )
        if form.logo.data:
            store.logo = save_picture(form.logo.data, 'stores')
        if form.banner.data:
            store.banner = save_picture(form.banner.data, 'stores')
        db.session.add(store)
        db.session.commit()
        flash('Store created successfully!', 'success')
        return redirect(url_for('seller.dashboard'))
    return render_template('seller/create_store.html', form=form, title='Create Store')


@seller_bp.route('/store/<int:store_id>/edit', methods=['GET', 'POST'])
def edit_store(store_id):
    store = Store.query.get_or_404(store_id)
    if store.owner_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller.dashboard'))

    form = StoreForm(obj=store)
    if form.validate_on_submit():
        store.name = form.name.data
        store.description = form.description.data
        if form.logo.data:
            store.logo = save_picture(form.logo.data, 'stores')
        if form.banner.data:
            store.banner = save_picture(form.banner.data, 'stores')
        db.session.commit()
        flash('Store updated successfully!', 'success')
        return redirect(url_for('seller.store_products', store_id=store.id))

    return render_template('seller/edit_store.html', form=form, store=store, title='Edit Store')


@seller_bp.route('/store/<int:store_id>/products')
def store_products(store_id):
    store = Store.query.get_or_404(store_id)
    if store.owner_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller.dashboard'))

    products = Product.query.filter_by(store_id=store.id).order_by(Product.created_at.desc()).all()
    return render_template('seller/store_products.html', store=store, products=products, title=f'{store.name} Products')


@seller_bp.route('/store/<int:store_id>/product/add', methods=['GET', 'POST'])
def add_product(store_id):
    store = Store.query.get_or_404(store_id)
    if store.owner_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller.dashboard'))

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            compare_price=form.compare_price.data,
            quantity=form.quantity.data,
            sku=form.sku.data,
            category=form.category.data,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data,
            store_id=store.id
        )
        if form.image.data:
            product.image = save_picture(form.image.data, 'products')
        if form.image2.data:
            product.image2 = save_picture(form.image2.data, 'products')
        if form.image3.data:
            product.image3 = save_picture(form.image3.data, 'products')

        db.session.add(product)
        db.session.commit()
        flash(f'Product "{product.name}" added successfully!', 'success')
        return redirect(url_for('seller.store_products', store_id=store.id))

    return render_template('seller/add_product.html', form=form, store=store, title='Add Product')


@seller_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    store = Store.query.get(product.store_id)
    if store.owner_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller.dashboard'))

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.compare_price = form.compare_price.data
        product.quantity = form.quantity.data
        product.sku = form.sku.data
        product.category = form.category.data
        product.is_featured = form.is_featured.data
        product.is_active = form.is_active.data

        if form.image.data:
            product.image = save_picture(form.image.data, 'products')
        if form.image2.data:
            product.image2 = save_picture(form.image2.data, 'products')
        if form.image3.data:
            product.image3 = save_picture(form.image3.data, 'products')

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('seller.store_products', store_id=store.id))

    return render_template('seller/edit_product.html', form=form, product=product, store=store, title='Edit Product')


@seller_bp.route('/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    store = Store.query.get(product.store_id)
    if store.owner_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller.dashboard'))

    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('seller.store_products', store_id=store.id))


@seller_bp.route('/orders')
def sales():
    stores = Store.query.filter_by(owner_id=current_user.id).all()
    if not stores:
        flash('Create a store first.', 'warning')
        return redirect(url_for('seller.create_store'))

    store_ids = [s.id for s in stores]
    page = request.args.get('page', 1, type=int)
    orders = OrderItem.query.filter(
        OrderItem.store_id.in_(store_ids)
    ).order_by(OrderItem.id.desc()).paginate(page=page, per_page=20)

    total_revenue = db.session.query(db.func.sum(OrderItem.subtotal)).filter(
        OrderItem.store_id.in_(store_ids)
    ).scalar() or 0

    return render_template('seller/sales.html', orders=orders, stores=stores,
                           total_revenue=total_revenue, title='Sales Overview')


@seller_bp.route('/order/<int:order_item_id>/status', methods=['POST'])
def update_order_status(order_item_id):
    order_item = OrderItem.query.get_or_404(order_item_id)
    store = Store.query.get(order_item.store_id)
    if not store or store.owner_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller.dashboard'))

    # Update parent order status
    order = Order.query.get(order_item.order_id)
    new_status = request.form.get('status')
    if new_status in ['processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}.', 'success')

    return redirect(url_for('seller.sales'))

