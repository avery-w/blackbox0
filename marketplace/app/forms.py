from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional
from app.models import User, Store


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[Length(max=150)])
    phone = StringField('Phone', validators=[Length(max=20)])
    address = TextAreaField('Address')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    compare_price = FloatField('Compare-at Price', validators=[Optional()])
    quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)], default=0)
    sku = StringField('SKU', validators=[Length(max=50)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing & Fashion'),
        ('home', 'Home & Garden'),
        ('beauty', 'Beauty & Health'),
        ('sports', 'Sports & Outdoors'),
        ('books', 'Books & Media'),
        ('food', 'Food & Beverages'),
        ('toys', 'Toys & Games'),
        ('automotive', 'Automotive'),
        ('other', 'Other')
    ])
    image = FileField('Main Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    image2 = FileField('Additional Image 2', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    image3 = FileField('Additional Image 3', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    is_featured = BooleanField('Featured Product')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Product')


class StoreForm(FlaskForm):
    name = StringField('Store Name', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description')
    logo = FileField('Store Logo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    banner = FileField('Store Banner', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    submit = SubmitField('Save Store')


class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('Shipping Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    payment_method = SelectField('Payment Method', choices=[
        ('cod', 'Cash on Delivery'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card')
    ], default='cod')
    notes = TextAreaField('Order Notes')
    submit = SubmitField('Place Order')


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(5, '5 - Excellent'), (4, '4 - Good'), (3, '3 - Average'), (2, '2 - Poor'), (1, '1 - Terrible')], coerce=int)
    comment = TextAreaField('Review', validators=[Length(max=1000)])
    submit = SubmitField('Submit Review')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing & Fashion'),
        ('home', 'Home & Garden'),
        ('beauty', 'Beauty & Health'),
        ('sports', 'Sports & Outdoors'),
        ('books', 'Books & Media'),
        ('food', 'Food & Beverages'),
        ('toys', 'Toys & Games'),
        ('automotive', 'Automotive'),
        ('other', 'Other')
    ])
    min_price = FloatField('Min Price', validators=[Optional()])
    max_price = FloatField('Max Price', validators=[Optional()])
    sort_by = SelectField('Sort By', choices=[
        ('newest', 'Newest'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('name_asc', 'Name: A-Z'),
        ('name_desc', 'Name: Z-A')
    ])
    submit = SubmitField('Search')

