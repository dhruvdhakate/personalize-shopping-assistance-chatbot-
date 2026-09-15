from flask import Flask, render_template
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

PRODUCTS = [
    {"id": 1, "name": "Apple iPhone 16", "category": "mobile", "price": 79999, "rating": 4.7, "image": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?auto=format&fit=crop&w=800&q=80"},
    {"id": 2, "name": "Samsung Galaxy S25", "category": "mobile", "price": 74999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80"},
    {"id": 3, "name": "Sony WH-1000XM5", "category": "headphones", "price": 29990, "rating": 4.8, "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80"},
    {"id": 4, "name": "Apple AirPods Pro", "category": "headphones", "price": 24900, "rating": 4.7, "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80"},
    {"id": 5, "name": "Nike Air Max 270", "category": "shoes", "price": 12995, "rating": 4.5, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80"},
    {"id": 6, "name": "Adidas Ultraboost", "category": "shoes", "price": 15999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80"},
    {"id": 7, "name": "MacBook Air M3", "category": "laptop", "price": 114900, "rating": 4.8, "image": "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?auto=format&fit=crop&w=800&q=80"},
    {"id": 8, "name": "Dell XPS 13", "category": "laptop", "price": 99990, "rating": 4.5, "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80"},
    {"id": 9, "name": "Canon EOS R50", "category": "camera", "price": 67999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80"},
    {"id": 10, "name": "JBL Flip 6", "category": "speaker", "price": 11999, "rating": 4.7, "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80"},
    {"id": 11, "name": "Kindle Paperwhite", "category": "tablet", "price": 14999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80"},
    {"id": 12, "name": "Apple Watch Series 10", "category": "watch", "price": 46900, "rating": 4.7, "image": "https://images.unsplash.com/photo-1551816230-ef5deaed4a26?auto=format&fit=crop&w=800&q=80"},
    {"id": 13, "name": "Sony Alpha A7 IV", "category": "camera", "price": 199990, "rating": 4.8, "image": "https://images.unsplash.com/photo-1510127034890-ba27508e9f1c?auto=format&fit=crop&w=800&q=80"},
    {"id": 14, "name": "Nike Air Force 1", "category": "shoes", "price": 9695, "rating": 4.7, "image": "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80"},
    {"id": 15, "name": "Logitech MX Master 3S", "category": "accessories", "price": 8995, "rating": 4.7, "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=800&q=80"},
    {"id": 16, "name": "Amazon Echo Dot", "category": "speaker", "price": 5499, "rating": 4.5, "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=800&q=80"},
    {"id": 17, "name": "Google Pixel 9", "category": "mobile", "price": 79999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=80"},
    {"id": 18, "name": "HP Pavilion 15", "category": "laptop", "price": 67990, "rating": 4.4, "image": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=800&q=80"},
]

KEYWORDS = {
    "mobile": ["mobile", "phone", "smartphone", "iphone", "samsung", "pixel"],
    "headphones": ["headphone", "headphones", "earphone", "earbuds", "airpods"],
    "shoes": ["shoe", "shoes", "sneaker", "sneakers", "running"],
    "laptop": ["laptop", "macbook", "computer", "notebook"],
    "camera": ["camera", "photography", "dslr", "mirrorless"],
    "speaker": ["speaker", "speakers", "sound"],
    "tablet": ["tablet", "kindle", "reading"],
    "watch": ["watch", "smartwatch"],
    "accessories": ["mouse", "accessory", "accessories"],
}

def detect_category(text):
    t = text.lower()
    for category, words in KEYWORDS.items():
        if any(w in t for w in words):
            return category
    return None

def extract_budget(text):
    nums = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', text.lower())
    values = []
    for n in nums:
        try:
            values.append(float(n.replace(",", "")))
        except:
            pass
    if not values:
        return None
    # Interpret "50k", "1 lakh", etc.
    if "lakh" in text.lower():
        return max(values) * 100000
    if "k" in text.lower() or "thousand" in text.lower():
        return max(values) * 1000
    return max(values)

def recommend(text):
    category = detect_category(text)
    budget = extract_budget(text)
    results = PRODUCTS[:]
    if category:
        results = [p for p in results if p["category"] == category]
    if budget:
        under = [p for p in results if p["price"] <= budget]
        if under:
            results = under
    results.sort(key=lambda p: (p["rating"], -p["price"]), reverse=True)
    return results[:6], category, budget

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/products")
def products():
    return jsonify(PRODUCTS)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"reply": "Please tell me what you want to shop for.", "products": []})

    results, category, budget = recommend(message)

    if category and budget:
        reply = f"I found {len(results)} {category} options around your budget of ₹{budget:,.0f}. Here are my best picks."
    elif category:
        reply = f"Here are some highly rated {category} options. I can also filter them by your budget."
    elif budget:
        reply = f"Here are highly rated products close to your ₹{budget:,.0f} budget. Tell me a category if you want more specific recommendations."
    else:
        reply = "Sure! Here are some popular picks. Try messages like “best phone under 50000” or “headphones under 30000”."

    return jsonify({"reply": reply, "products": results})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
