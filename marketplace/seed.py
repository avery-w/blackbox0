"""Seed script to populate the database with sample data for testing."""
from app import create_app, db
from app.models import User, Store, Product, Review
import random

app = create_app()

with app.app_context():
    # Check if already seeded
    if User.query.first():
        print("Database already contains data. Skipping seed.")
        exit()

    # Create admin user
    admin = User(
        username='admin',
        email='admin@markethub.com',
        full_name='Admin User',
        is_seller=True,
        is_admin=True,
        address='123 Admin Street, City, State 12345',
        phone='+1-555-0100'
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # Create seller users
    sellers_data = [
        {'username': 'techseller', 'email': 'tech@seller.com', 'full_name': 'Tech Gadgets Seller', 'store_name': 'Tech Haven', 'store_desc': 'Your one-stop shop for the latest electronics and gadgets.'},
        {'username': 'fashionseller', 'email': 'fashion@seller.com', 'full_name': 'Fashion Designer', 'store_name': 'Fashion Forward', 'store_desc': 'Trendy clothing and accessories for every style.'},
        {'username': 'homeseller', 'email': 'home@seller.com', 'full_name': 'Home Decor Expert', 'store_name': 'Home & Cozy', 'store_desc': 'Beautiful home decor and garden essentials.'},
        {'username': 'beautyseller', 'email': 'beauty@seller.com', 'full_name': 'Beauty Specialist', 'store_name': 'Glow Beauty', 'store_desc': 'Premium beauty and health products.'},
        {'username': 'bookseller', 'email': 'books@seller.com', 'full_name': 'Book Lover', 'store_name': 'Page Turners', 'store_desc': 'Curated collection of books and media.'},
    ]

    sellers = []
    for s_data in sellers_data:
        seller = User(
            username=s_data['username'],
            email=s_data['email'],
            full_name=s_data['full_name'],
            is_seller=True,
            address='123 Seller Street, City, State 12345',
            phone='+1-555-0101'
        )
        seller.set_password('seller123')
        db.session.add(seller)
        sellers.append(seller)

    # Create regular users
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'full_name': 'John Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'full_name': 'Jane Smith'},
        {'username': 'bob_wilson', 'email': 'bob@example.com', 'full_name': 'Bob Wilson'},
    ]
    users = []
    for u_data in users_data:
        user = User(
            username=u_data['username'],
            email=u_data['email'],
            full_name=u_data['full_name'],
            address='456 Customer Ave, City, State 12345',
            phone='+1-555-0200'
        )
        user.set_password('user123')
        db.session.add(user)
        users.append(user)

    db.session.flush()

    # Create stores
    stores = []
    for i, s_data in enumerate(sellers_data):
        store = Store(
            name=s_data['store_name'],
            description=s_data['store_desc'],
            owner_id=sellers[i].id,
            is_active=True
        )
        db.session.add(store)
        stores.append(store)

    db.session.flush()

    # Create products
    products_data = [
        # Tech Haven products
        {'name': 'Wireless Bluetooth Headphones', 'desc': 'Premium noise-cancelling wireless headphones with 30hr battery life. Features high-fidelity audio and comfortable over-ear design.', 'price': 149.99, 'compare_price': 199.99, 'qty': 50, 'category': 'electronics', 'store_idx': 0, 'featured': True},
        {'name': 'Smart Watch Pro', 'desc': 'Advanced smartwatch with health monitoring, GPS tracking, and 7-day battery life. Water resistant to 50m.', 'price': 249.99, 'compare_price': 299.99, 'qty': 30, 'category': 'electronics', 'store_idx': 0, 'featured': True},
        {'name': 'USB-C Hub 7-in-1', 'desc': 'Compact USB-C hub with HDMI, USB 3.0, SD card reader, and PD charging. Compatible with all USB-C devices.', 'price': 39.99, 'qty': 100, 'category': 'electronics', 'store_idx': 0},
        {'name': 'Mechanical Keyboard RGB', 'desc': 'Full-size mechanical keyboard with customizable RGB lighting and Cherry MX switches. Durable aluminum frame.', 'price': 89.99, 'compare_price': 119.99, 'qty': 45, 'category': 'electronics', 'store_idx': 0},

        # Fashion Forward products
        {'name': 'Classic Denim Jacket', 'desc': 'Timeless denim jacket made from premium cotton. Features a comfortable fit and classic styling.', 'price': 79.99, 'compare_price': 99.99, 'qty': 40, 'category': 'clothing', 'store_idx': 1, 'featured': True},
        {'name': 'Casual Sneakers White', 'desc': 'Minimalist white sneakers made with sustainable materials. Comfortable for all-day wear.', 'price': 64.99, 'qty': 60, 'category': 'clothing', 'store_idx': 1},
        {'name': 'Wool Blend Scarf', 'desc': 'Luxuriously soft wool blend scarf in classic plaid pattern. Measures 70" x 12".', 'price': 34.99, 'compare_price': 49.99, 'qty': 75, 'category': 'clothing', 'store_idx': 1},
        {'name': 'Leather Crossbody Bag', 'desc': 'Genuine leather crossbody bag with adjustable strap and multiple compartments. Perfect for everyday use.', 'price': 129.99, 'qty': 25, 'category': 'clothing', 'store_idx': 1},

        # Home & Cozy products
        {'name': 'Scented Candles Set', 'desc': 'Set of 3 hand-poured soy candles in vanilla, lavender, and eucalyptus. Each burns for 45+ hours.', 'price': 29.99, 'qty': 80, 'category': 'home', 'store_idx': 2, 'featured': True},
        {'name': 'Bamboo Plant Stand', 'desc': 'Elegant bamboo plant stand with 3 tiers. Holds up to 6 small plants. Eco-friendly and sturdy.', 'price': 44.99, 'compare_price': 54.99, 'qty': 35, 'category': 'home', 'store_idx': 2},
        {'name': 'Throw Blanket Premium', 'desc': 'Ultra-soft microfiber throw blanket. Machine washable. Available in multiple colors. 50" x 60".', 'price': 39.99, 'qty': 55, 'category': 'home', 'store_idx': 2},

        # Glow Beauty products
        {'name': 'Vitamin C Serum', 'desc': 'Powerful antioxidant serum with 20% Vitamin C, hyaluronic acid, and vitamin E. Brightens and evens skin tone.', 'price': 28.99, 'compare_price': 39.99, 'qty': 65, 'category': 'beauty', 'store_idx': 3, 'featured': True},
        {'name': 'Organic Face Moisturizer', 'desc': 'Lightweight organic face moisturizer with SPF 30. Suitable for all skin types. Made with natural ingredients.', 'price': 24.99, 'qty': 70, 'category': 'beauty', 'store_idx': 3},
        {'name': 'Essential Oil Diffuser', 'desc': 'Ultrasonic aromatherapy diffuser with LED lights. Covers up to 500 sq ft. Runs for 8+ hours.', 'price': 32.99, 'compare_price': 42.99, 'qty': 40, 'category': 'beauty', 'store_idx': 3},

        # Page Turners products
        {'name': 'The Art of Coding', 'desc': 'A comprehensive guide to modern software development practices. Covers Python, JavaScript, and best practices.', 'price': 34.99, 'qty': 90, 'category': 'books', 'store_idx': 4, 'featured': True},
        {'name': 'Mystery at Midnight', 'desc': 'A gripping mystery novel that will keep you on the edge of your seat. Bestselling author.', 'price': 19.99, 'compare_price': 24.99, 'qty': 85, 'category': 'books', 'store_idx': 4},
        {'name': 'Cookbook: Global Flavors', 'desc': 'Explore cuisines from around the world with 200+ easy-to-follow recipes. Beautifully photographed.', 'price': 29.99, 'qty': 50, 'category': 'books', 'store_idx': 4},
    ]

    products = []
    for p_data in products_data:
        product = Product(
            name=p_data['name'],
            description=p_data['desc'],
            price=p_data['price'],
            compare_price=p_data.get('compare_price'),
            quantity=p_data['qty'],
            category=p_data['category'],
            store_id=stores[p_data['store_idx']].id,
            is_featured=p_data.get('featured', False),
            is_active=True,
            sku=f"SKU-{p_data['store_idx']}-{p_data['name'][:3].upper()}-{random.randint(100, 999)}"
        )
        db.session.add(product)
        products.append(product)

    db.session.flush()

    # Add some reviews
    review_texts = [
        'Excellent product! Exceeded my expectations.',
        'Great quality and fast shipping. Highly recommend!',
        'Good product for the price. Would buy again.',
        'Decent quality, but could be better.',
        'Amazing! Better than described.',
        'Love this product! Already recommended to friends.',
        'Good value for money. Satisfied with purchase.',
    ]

    for i, product in enumerate(products[:10]):  # Review first 10 products
        reviewer = users[i % len(users)]
        review = Review(
            rating=random.randint(3, 5),
            comment=random.choice(review_texts),
            user_id=reviewer.id,
            product_id=product.id
        )
        db.session.add(review)

        # Add a second review for some products
        if i % 2 == 0:
            review2 = Review(
                rating=random.randint(4, 5),
                comment=random.choice(review_texts),
                user_id=users[(i + 1) % len(users)].id,
                product_id=product.id
            )
            db.session.add(review2)

    db.session.commit()
    print("Database seeded successfully!")
    print(f"\nCreated: {User.query.count()} users, {Store.query.count()} stores, {Product.query.count()} products, {Review.query.count()} reviews")
    print("\nLogin Credentials:")
    print("  Admin: admin@markethub.com / admin123")
    print("  Seller: tech@seller.com / seller123")
    print("  User: john@example.com / user123")

