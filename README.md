# 🍽️ FoodOrder — Django Food Ordering Web App

A full-featured food ordering web application built with Django, featuring a beautiful modern UI with HTML, CSS, and JavaScript.

---

## 📁 Project Structure

```
foodorder/
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
├── setup.sh                          # One-click setup script
├── db.sqlite3                        # SQLite database (auto-created)
│
├── foodorder/                        # Main project config
│   ├── __init__.py
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Root URL configuration
│   ├── wsgi.py                       # WSGI server entry point
│   └── asgi.py                       # ASGI server entry point
│
├── restaurant/                       # Main app
│   ├── __init__.py
│   ├── models.py                     # Database models
│   ├── views.py                      # View logic
│   ├── urls.py                       # App URLs
│   ├── auth_urls.py                  # Auth URLs
│   ├── forms.py                      # Django forms
│   ├── admin.py                      # Admin configuration
│   ├── apps.py                       # App config
│   ├── context_processors.py         # Template context
│   ├── migrations/                   # Database migrations
│   └── fixtures/
│       └── initial_data.json         # Sample menu data
│
├── static/
│   ├── css/
│   │   └── main.css                  # Main stylesheet
│   └── js/
│       └── main.js                   # JavaScript (AJAX, cart, etc.)
│
└── templates/
    ├── base.html                     # Base template (navbar, footer)
    ├── restaurant/
    │   ├── home.html                 # Landing page
    │   ├── menu.html                 # Menu listing with filters
    │   ├── item_detail.html          # Single item + reviews
    │   ├── cart.html                 # Shopping cart
    │   ├── checkout.html             # Checkout form
    │   ├── order_list.html           # User's orders
    │   ├── order_detail.html         # Order tracking
    │   └── profile.html             # User profile
    └── registration/
        ├── login.html                # Login page
        └── register.html            # Registration page
```

---

## 🚀 Quick Setup

### Option 1: Automated Script
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Load sample data
python manage.py loaddata restaurant/fixtures/initial_data.json

# 5. Create admin user
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**  
Admin: **http://127.0.0.1:8000/admin/**

---

## 🌟 Features

| Feature | Details |
|---------|---------|
| 🏠 **Home Page** | Hero section, featured dishes, categories, how-it-works |
| 📋 **Menu** | Grid layout, category filter, search, veg/spicy filters |
| 🔍 **Item Detail** | Full info, related items, customer reviews |
| 🛒 **Cart** | AJAX add/remove/update, real-time totals |
| 💳 **Checkout** | Delivery info, payment method selection, order summary |
| 📦 **Order Tracking** | Visual progress tracker, status updates |
| 👤 **User Profiles** | Avatar, saved address, order history |
| 🔑 **Auth** | Register, login, logout with secure sessions |
| 🔧 **Admin Panel** | Full CRUD for menu, orders, categories |

---

## 🗄️ Database Models

- **Category** — Food categories (Pizza, Burgers, etc.)
- **MenuItem** — Food items with pricing, images, flags
- **Cart / CartItem** — User shopping carts
- **Order / OrderItem** — Completed orders
- **UserProfile** — Extended user info
- **Review** — Item reviews with star ratings

---

## ⚙️ Configuration

Edit `foodorder/settings.py`:
- `SECRET_KEY` — Change for production
- `DEBUG` — Set to `False` in production
- `DATABASES` — Switch to PostgreSQL for production
- `STRIPE_PUBLIC_KEY` / `STRIPE_SECRET_KEY` — Add your Stripe keys

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Python 3.10+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Bootstrap 5, Custom CSS, Vanilla JS
- **Forms**: django-crispy-forms + crispy-bootstrap5
- **Images**: Pillow
- **Static**: WhiteNoise
- **Payments**: Stripe (configured, ready to wire up)
"# Food-Order-Web" 
