# AaplaBazaar - Indian E-commerce Platform

AaplaBazaar is an e-commerce platform for authentic Indian products, supporting features such as user authentication, shopping cart, wishlists, order tracking, SMS notifications, and secure payments.

## Features

- User registration, login, and profile management
- Product browsing by category (Jewelry, Spices, Home Decor, Food Products, etc.)
- Shopping cart with quantity management and cart total calculation
- Wishlist functionality with AJAX support
- Order checkout with address autofill and payment method selection (Cash on Delivery, Stripe integration)
- Order tracking and SMS notifications via Twilio
- Easy returns and 24/7 customer support
- Responsive design with Bootstrap and Swiper slider

## Tech Stack

- **Backend:** Flask (Python), Flask-WTF, Flask-Login, Flask-SQLAlchemy
- **Frontend:** HTML, CSS (Bootstrap), JavaScript (with Swiper, Font Awesome)
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **SMS Notifications:** Twilio API
- **Payments:** Stripe API
- **Deployment:** Gunicorn

## Project Structure

```
├── app.py
├── models.py
├── forms.py
├── routes.py
├── utils.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── wishlist.html
│   ├── profile.html
│   ├── update_profile.html
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   │   ├── main.js
│   │   ├── cart.js
│   │   ├── wishlist.js
│   │   └── slider.js
│   └── ...
├── instance/
│   └── aaplabazaar.db
├── pyproject.toml
└── README.md
```

## Getting Started

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set up environment variables:**  
   Configure your `.env.py` and `utils.env.txt` for database and API keys.

3. **Run the application:**
   ```sh
   flask run
   ```

4. **Access the app:**  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## License

MIT License

---

For more details, see the source files:  
- [app.py](app.py)  
- [models.py](models.py)  
- [routes.py](routes.py)  
