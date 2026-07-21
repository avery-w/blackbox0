from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.models import Product, Review, Store
from app.forms import ReviewForm, SearchForm
from app import db
from flask_login import current_user, login_required

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/')
def browse():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'newest')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    q = request.args.get('q', '')

    query = Product.query.filter_by(is_active=True)

    if q:
        query = query.filter(Product.name.ilike(f'%{q}%') | Product.description.ilike(f'%{q}%'))
    if category:
        query = query.filter_by(category=category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Product.name.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    categories = [
        ('electronics', 'Electronics'), ('clothing', 'Clothing & Fashion'),
        ('home', 'Home & Garden'), ('beauty', 'Beauty & Health'),
        ('sports', 'Sports & Outdoors'), ('books', 'Books & Media'),
        ('food', 'Food & Beverages'), ('toys', 'Toys & Games'),
        ('automotive', 'Automotive'), ('other', 'Other')
    ]
    return render_template('products/browse.html', products=products, categories=categories,
                           category=category, sort_by=sort_by, q=q, title='Browse Products')


@products_bp.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter_by(category=product.category, is_active=True)\
        .filter(Product.id != product.id).order_by(Product.created_at.desc()).limit(4).all()
    form = ReviewForm()

    # Get store products
    store_products = Product.query.filter_by(store_id=product.store_id, is_active=True)\
        .filter(Product.id != product.id).limit(4).all()

    # Calculate average rating
    avg_rating = product.average_rating
    rating_counts = {i: 0 for i in range(1, 6)}
    for review in product.reviews:
        if review.rating in rating_counts:
            rating_counts[review.rating] += 1

    return render_template('products/detail.html', product=product, related=related,
                           store_products=store_products, form=form,
                           avg_rating=avg_rating, rating_counts=rating_counts, title=product.name)


@products_bp.route('/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    if form.validate_on_submit():
        # Check if user already reviewed
        existing = Review.query.filter_by(user_id=current_user.id, product_id=product.id).first()
        if existing:
            existing.rating = form.rating.data
            existing.comment = form.comment.data
            flash('Your review has been updated!', 'success')
        else:
            review = Review(
                rating=form.rating.data,
                comment=form.comment.data,
                user_id=current_user.id,
                product_id=product.id
            )
            db.session.add(review)
            flash('Your review has been submitted!', 'success')
        db.session.commit()
    return redirect(url_for('products.detail', product_id=product.id))

