# ShopMate AI — Personalized Shopping Assistant

A beginner-friendly shopping chatbot made with **Python (Flask) + HTML + CSS + JavaScript**.

## Features
- Personalized shopping chatbot
- 18 sample products
- Real product-style images loaded from Unsplash
- Product name, category, price and rating
- Category detection (mobile, laptop, shoes, headphones, camera, etc.)
- Budget filtering such as `best phone under 50000`
- Responsive design for desktop and mobile
- No database required

## Run on Windows

Open Command Prompt / PowerShell inside this project folder:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

## Example messages
- best phone under 50000
- headphones under 30000
- best laptop under 100000
- shoes under 15000
- best camera
- show me a smartwatch

## Important
The images are loaded from Unsplash URLs, so an internet connection is needed for the real images to appear. The product data is demo data and should be replaced with your actual catalog before production use.
