from flask import Flask, flash, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from math import ceil

import os
app = Flask(__name__)
products=[]
app.config['UPLOAD_FOLDER'] = 'static/uploads'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'  # Using SQLite for simplicity
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/products.db'  # For storing in a 'data' folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids overhead warnings
db = SQLAlchemy(app)
app.secret_key = '64b91608d925bad4e472b7c795da200b'

@app.before_request
def create_tables():
    db.create_all()

hardcoded_product = [
        {
            'id': 1,
            'name': 'Custom Rubber Stamp',
            'description': 'Personalize your stamp with any text.',
            'price': 'Rs.100',
            'rating': 4.5,
            'image': 'custom-stamp.jpg',
            'reviews': ['Great product!', 'Highly recommended!'],
            'models': ['Round', 'Square', 'Rectangle']
        },
        {
            'id': 2,
            'name': 'Logo Rubber Stamp',
            'description': 'Perfect for branding your business materials.',
            'price': 'Rs.150',
            'rating': 4.0,
            'image': 'logo-stamp.jpg',
            'reviews': ['Nice and crisp.', 'Affordable and durable.'],
            'models': ['Round', 'Square']
        },
        {
            'id': 3,
            'name': 'Ink Pad',
            'description': 'High-quality ink pad for rubber stamps.',
            'price': 'Rs.50',
            'rating': 4.2,
            'image': 'ink-pad.jpg',
            'reviews': ['Good condition and durability', 'Affordable'],
            'models': ['Round', 'Square']
        },
        {
            'id': 4,
            'name': 'Self-Ink Rubber Stamp',
            'description': 'Good-quality, durable self-ink rubber stamps.',
            'price': 'Rs.150',
            'rating': 4.4,
            'image': 'self-ink.jpg',
            'reviews': ['Good condition and durability', 'Affordable'],
            'models': ['Rectangular', 'Square']
        },
        {
            'id': 5,
            'name': 'Printto Dater Stamp',
            'description': 'Good-quality dater rubber stamps.',
            'price': 'Rs.450',
            'rating': 4.0,
            'image': 'dater-stamp.jpg',
            'reviews': ['Good condition and durability', 'Affordable'],
            'models': ['Teacher Use', 'Cancelled']
        },
        {
            'id': 6,
            'name': 'Shiny S-882 Self-Inking DIY Ink Set',
            'description': 'DIY Ink Set.',
            'price': 'Rs.550',
            'rating': 4.7,
            'image': 'diy-set.jpg',
            'reviews': ['Creative and Useful', 'Affordable'],
            'models': ['Customised']
        },
        {
            'id': 7,
            'name': 'Envelope Rubber Stamp',
            'description': 'Stamp for Envelopes',
            'price': 'Rs.250',
            'rating': 4.4,
            'image': 'envelope.jpg',
            'reviews': ['Good quality', 'Affordable'],
            'models': ['Colors: Red, Black, Blue']
        },
        {
            'id': 8,
            'name': 'Office Stamp',
            'description': 'Ease of use, Replaceable, Refillable and Easy Removal Ink Pad',
            'price': 'Rs.650',
            'rating': 4.8,
            'image': 'office.jpg',
            'reviews': ['Durable', 'Affordable'],
            'models': ['231AB', 'KDJ78']
        }
    ]
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # Relationship to store reviews for each user
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(500), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    product = db.relationship('Product', backref='reviews', lazy=True)

    def __repr__(self):
        return f'<Review {self.id} for Product {self.product_id}>'

# Define the Product model
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'

# Route to add a product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        image = request.files['image']
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f'uploads/{filename}'
        else:
            image_url = None

                # Create new Product object and save it to the database
        new_product = Product(
            name=name, 
            description=description, 
            price=price, 
            quantity=quantity, 
            image=image_url
        )
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('view_products'))  # Redirect to product list page after adding

    return render_template('add_product.html')

@app.route('/splash')
def splash():
    return render_template('splash.html')


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image = f'uploads/{filename}'

        db.session.commit()
        return redirect(url_for('view_products'))

    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('view_products'))
@app.route('/view_products')
def view_products():
    # Fetch products from the database
    db_products = Product.query.all()

    # Convert database products to a format similar to hardcoded products
    db_products_formatted = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': f"Rs.{product.price}",
            'rating': None,  # Add ratings if applicable
            'image': product.image,
            'reviews': [],  # Add reviews if applicable
            'models': []    # Add models if applicable
        }
        for product in db_products
    ]

    # Combine hardcoded products and database products
    all_products = hardcoded_product + db_products_formatted

    # Render the template
    return render_template('view_products.html', products=all_products)
USER_CREDENTIALS = {'username': 'admin', 'password': 'password123'}
users = []  # List to store dynamically signed-up users

@app.route('/admin', methods=['GET'])
def admin_panel():
    return render_template('admin.html')
@app.route('/')
def index():
    return redirect('/splash')
@app.route('/home')
def home():
    is_admin = session.get('is_admin', False)  # Default to False
    return render_template('index.html', is_admin=is_admin)
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))
@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    print("About Us route accessed!")
    return render_template('about_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    print("Contact Us route accessed!")
    return render_template('contact_us.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Check if the user is the admin using hardcoded credentials
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['logged_in'] = True
            session['is_admin'] = True  # Mark as admin
            return redirect(url_for('home'))  # Redirect to admin panel

        # Check the user credentials in the database
        user = User.query.filter_by(email=username, password=password).first()
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id  # Store user id in the session
            session['is_admin'] = False  # Regular user by default
            return redirect(url_for('home'))  # Redirect to home page

        error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name'].strip()
        phone = request.form['phone'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Create a new user in the database
        new_user = User(name=name, phone=phone, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Redirect to the login page after successful sign-up
    return render_template('sign_up.html')


@app.route('/logout')
def logout():
    # Remove 'logged_in' status from the session
    session.pop('logged_in', None)
    flash('Successfully logged out')  # Add a flash message
    return redirect(url_for('login'))  # Redirect to the login pag

@app.route('/products')
def products_page():
    # Get search query and pagination parameters
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))  # Current page, default is 1
    per_page = 4  # Number of products per page

    # Base query for fetching products
    product_query = Product.query

    # Apply search filters if a query exists
    if query:
        product_query = product_query.filter(
            Product.name.ilike(f"%{query}%") | Product.description.ilike(f"%{query}%")
        )

    # Get total count and apply pagination
    total_products = product_query.count()
    total_pages = ceil(total_products / per_page)

    # Fetch paginated results
    db_products = product_query.offset((page - 1) * per_page).limit(per_page).all()

    # Format database products
    paginated_products = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': f"Rs.{product.price}",
            'rating': product.rating if hasattr(product, 'rating') else None,  # Add ratings if applicable
            'image': product.image,
            'reviews': product.reviews if hasattr(product, 'reviews') else [],  # Add reviews if applicable
            'models': product.models if hasattr(product, 'models') else []    # Add models if applicable
        }
        for product in db_products
    ]

    # Render the products page
    return render_template(
        'products.html',
        products=paginated_products,
        page=page,
        total_pages=total_pages,
        query=query  # Pass the query to maintain search context
    )

# Example route fix
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    if 'logged_in' in session and session['logged_in']:
        product = Product.query.get(product_id)
        if product:
            reviews = Review.query.filter_by(product_id=product_id).all()
            print(f"Reviews for product {product_id}: {reviews}")  # Debugging line to see reviews in the console
            return render_template('product_detail.html', product=product, reviews=reviews)

        return redirect(url_for('products_page'))
    
    return redirect(url_for('login'))


@app.route('/cart')
def cart_page():
    if 'logged_in' in session and session['logged_in']:
        cart_items = session.get('cart', [])
        return render_template('cart.html', cart_items=cart_items)
    return redirect(url_for('login'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'logged_in' in session and session['logged_in']:
        product = Product.query.get(product_id)
        if product:
            if 'cart' not in session:
                session['cart'] = []
            
            # Check if the product already exists in the cart
            item_exists = False
            for item in session['cart']:
                if item['id'] == product.id:
                    item['quantity'] += 1  # Increment quantity if product exists
                    item_exists = True
                    break

            # Add the product if it doesn't exist in the cart
            if not item_exists:
                session['cart'].append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': 1
                })
            
            session.modified = True
        
        return redirect(url_for('cart_page'))
    return redirect(url_for('login'))

@app.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    if 'logged_in' in session and session['logged_in']:
        # Get the review text from the form
        review_text = request.form['review']
        
        # Get the user ID from the session (assuming it's stored in the session when logged in)
        user_id = session.get('user_id')  # Ensure you have user_id stored in session during login

        if not review_text:
            flash("Review cannot be empty.")
            return redirect(url_for('product_detail', product_id=product_id))
        

        # Create a new review and add it to the database
        new_review = Review(review=review_text, product_id=product_id, user_id=user_id)

        try:
            db.session.add(new_review)
            db.session.commit()  # Save the new review to the database
            flash("Review submitted successfully!")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"An error occurred while submitting your review: {e}")

        return redirect(url_for('product_detail', product_id=product_id))
    
    return redirect(url_for('login'))  # Redirect to login page if user is not logged in


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'logged_in' in session and session['logged_in']:
        if 'cart' in session:
            # Safely filter items in the cart
            session['cart'] = [item for item in session['cart'] if item.get('id') != product_id]
            session.modified = True
        return redirect(url_for('cart_page'))
    return redirect(url_for('login'))


@app.route('/buy_now/<int:product_id>', methods=['GET', 'POST'])
def buy_now(product_id):
    if 'logged_in' in session and session['logged_in']:
        product = Product.query.get(product_id)
        if product:
            if request.method == 'POST':
                payment_method = request.form['payment_method']
                return redirect(url_for('order_confirmation', product_id=product_id, payment_method=payment_method))
            return render_template('buy_now.html', product=product)
        return redirect(url_for('products_page'))
    return redirect(url_for('login'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    if 'logged_in' in session and session['logged_in']:
        # Get the updated quantity from the form
        new_quantity = int(request.form['quantity'])
        
        # Check if the cart exists in the session
        if 'cart' in session:
            for item in session['cart']:
                if item['id'] == product_id:
                    # Update the quantity and recalculate the total price
                    item['quantity'] = new_quantity
                    item['total_price'] = item['price'] * new_quantity  # Store the updated price
                    break
            session.modified = True

        return redirect(url_for('cart_page'))
    return redirect(url_for('login'))


@app.route('/order_confirmation/<int:product_id>/<payment_method>', methods=['GET'])
def order_confirmation(product_id, payment_method):
    if 'logged_in' in session and session['logged_in']:
        product = Product.query.get(product_id)
        if product:
            # Here you can add logic to store the order in a database if needed
            return render_template('order_confirmation.html', product=product, payment_method=payment_method)
        return redirect(url_for('products_page'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)