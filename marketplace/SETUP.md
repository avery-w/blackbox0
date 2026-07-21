# MarketHub - E-Commerce Marketplace

A full-featured e-commerce marketplace web application built with Python Flask. Supports buyers, sellers, and administrators.

## Features

### Customer Features
- Browse products by category with search and filters
- User registration and login
- Shopping cart management (add, update, remove items)
- Order placement and management
- Product reviews and ratings
- User profile management

### Seller Features
- Create and manage multiple stores
- Add/edit/delete products with image uploads
- Track inventory and sales
- View and update order statuses
- Sales dashboard with statistics

### Admin Features
- Admin dashboard with system overview
- Manage users (promote to seller/admin)
- Manage stores (activate/deactivate)
- Manage products (activate/deactivate)
- Manage all orders (update statuses)

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-Login + Flask-Bcrypt
- **Forms**: Flask-WTF + WTForms
- **Image Processing**: Pillow
- **Frontend**: Responsive HTML/CSS with custom CSS framework
- **Icons**: Font Awesome 6

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or navigate to the project
```bash
cd marketplace
```

### Step 2: Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Seed the database (optional, creates sample data)
```bash
python seed.py
```

### Step 5: Run the application
```bash
python run.py
```

### Step 6: Open in browser
Navigate to: **http://localhost:5000**

## Default Accounts

After running `seed.py`, the following accounts are available:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@markethub.com | admin123 |
| Seller 1 | tech@seller.com | seller123 |
| Seller 2 | fashion@seller.com | seller123 |
| Seller 3 | home@seller.com | seller123 |
| Seller 4 | beauty@seller.com | seller123 |
| Seller 5 | books@seller.com | seller123 |
| Buyer | john@example.com | user123 |
| Buyer | jane@example.com | user123 |
| Buyer | bob@example.com | user123 |

## Project Structure

```
marketplace/
├── run.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── seed.py                 # Database seeding script
├── SETUP.md                # This file
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # Database models
│   ├── forms.py            # WTForms form definitions
│   ├── utils.py            # Utility functions
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication routes
│   │   ├── main.py         # Homepage and static pages
│   │   ├── products.py     # Product browsing routes
│   │   ├── cart.py         # Shopping cart routes
│   │   ├── orders.py       # Order management routes
│   │   ├── seller.py       # Seller dashboard routes
│   │   └── admin.py        # Admin panel routes
│   ├── templates/
│   │   ├── base.html       # Base template with nav/footer
│   │   ├── home.html       # Homepage
│   │   ├── about.html      # About page
│   │   ├── contact.html    # Contact page
│   │   ├── auth/           # Auth templates
│   │   ├── products/       # Product templates
│   │   ├── cart/           # Cart templates
│   │   ├── orders/         # Order templates
│   │   ├── seller/         # Seller templates
│   │   └── admin/          # Admin templates
│   └── static/
│       ├── css/style.css   # Custom CSS
│       ├── js/main.js      # JavaScript
│       └── uploads/        # Uploaded images
```

## Deployment

For production deployment:

1. Set a strong `SECRET_KEY` environment variable
2. Change `SQLALCHEMY_DATABASE_URI` to use PostgreSQL or MySQL
3. Set `DEBUG=False`
4. Use a production WSGI server like Gunicorn
5. Configure proper file serving for static/uploads

## API Endpoints

### Public
- `GET /` - Homepage
- `GET /products` - Browse products
- `GET /products/<id>` - Product detail

### Authentication
- `GET/POST /auth/register` - Register
- `GET/POST /auth/login` - Login
- `GET /auth/logout` - Logout
- `GET/POST /auth/profile` - Profile management

### Cart (requires login)
- `GET /cart/` - View cart
- `POST /cart/add/<id>` - Add to cart
- `POST /cart/update/<id>` - Update quantity
- `POST /cart/remove/<id>` - Remove item
- `POST /cart/clear` - Clear cart

### Orders (requires login)
- `GET/POST /orders/checkout` - Checkout
- `GET /orders/` - My orders
- `GET /orders/<id>` - Order detail
- `POST /orders/<id>/cancel` - Cancel order

### Seller (requires seller role)
- `GET /seller/` - Dashboard
- `GET/POST /seller/store/create` - Create store
- `GET/POST /seller/store/<id>/edit` - Edit store
- `GET /seller/store/<id>/products` - Store products
- `GET/POST /seller/store/<id>/product/add` - Add product
- `GET/POST /seller/product/<id>/edit` - Edit product
- `POST /seller/product/<id>/delete` - Delete product
- `GET /seller/orders` - Sales overview

### Admin (requires admin role)
- `GET /admin/` - Dashboard
- `GET /admin/users` - Manage users
- `GET /admin/stores` - Manage stores
- `GET /admin/products` - Manage products
- `GET /admin/orders` - Manage orders

