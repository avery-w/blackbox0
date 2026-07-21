from flask import Blueprint, render_template, request, current_app
from app.models import Product, Store, Review

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    featured = Product.query.filter_by(is_featured=True, is_active=True).order_by(Product.created_at.desc()).limit(8).all()
    newest = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(12).all()
    stores = Store.query.filter_by(is_active=True).order_by(Store.created_at.desc()).limit(6).all()
    return render_template('home.html', featured=featured, newest=newest, stores=stores, title='Home')


@main_bp.route('/about')
def about():
    return render_template('about.html', title='About Us')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

