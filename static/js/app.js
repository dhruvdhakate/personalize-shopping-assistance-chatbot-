const productsEl = document.getElementById("products");
const countEl = document.getElementById("count");
const chatEl = document.getElementById("chat");
const form = document.getElementById("chatForm");
const input = document.getElementById("message");

function money(n) {
  return new Intl.NumberFormat("en-IN", { style:"currency", currency:"INR", maximumFractionDigits:0 }).format(n);
}

function renderProducts(products) {
  countEl.textContent = `${products.length} product${products.length === 1 ? "" : "s"}`;
  productsEl.innerHTML = products.map(p => `
    <article class="card">
      <img src="${p.image}" alt="${p.name}" loading="lazy"
           onerror="this.src='https://placehold.co/800x500?text=Product+Image'">
      <div class="card-body">
        <div class="category">${p.category}</div>
        <h3>${p.name}</h3>
        <div class="price">${money(p.price)}</div>
        <div class="rating">★ ${p.rating} / 5</div>
      </div>
    </article>
  `).join("");
}

function addMessage(text, who="bot") {
  const row = document.createElement("div");
  row.className = `message ${who}`;
  row.innerHTML = `<div class="bubble">${text}</div>`;
  chatEl.appendChild(row);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function loadProducts() {
  const res = await fetch("/api/products");
  const products = await res.json();
  renderProducts(products);
}

async function sendMessage(text) {
  if (!text.trim()) return;
  addMessage(text, "user");
  input.value = "";
  addMessage("Finding the best matches for you…", "bot");
  const loading = chatEl.lastElementChild;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message:text})
    });
    const data = await res.json();
    loading.remove();
    addMessage(data.reply, "bot");
    renderProducts(data.products);
  } catch (e) {
    loading.remove();
    addMessage("Sorry, I could not connect to the shopping assistant. Please try again.", "bot");
  }
}

form.addEventListener("submit", e => {
  e.preventDefault();
  sendMessage(input.value);
});

function usePrompt(text) {
  input.value = text;
  sendMessage(text);
}

loadProducts();
