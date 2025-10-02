// Simple WebApp for Telegram
const tg = window.Telegram.WebApp;
tg.expand();

// Example product catalog
const products = [
  {id:1, name:"Футболка Classic", price:500},
  {id:2, name:"Худі Cozy", price:1200},
  {id:3, name:"Джинси Regular", price:1500},
  {id:4, name:"Кепка Sport", price:300}
];

const catalogEl = document.getElementById('catalog');
const cartEl = document.getElementById('cart');
const totalEl = document.getElementById('total');
const checkoutBtn = document.getElementById('checkoutBtn');
const modal = document.getElementById('checkoutModal');
const closeModal = document.getElementById('closeModal');
const sendOrderBtn = document.getElementById('sendOrder');

let cart = [];

function renderCatalog(){
  catalogEl.innerHTML = '';
  products.forEach(p=>{
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `<strong>${p.name}</strong><div>${p.price} грн</div><button data-id="${p.id}">Додати</button>`;
    catalogEl.appendChild(card);
  });
  catalogEl.querySelectorAll('button').forEach(b=>{
    b.addEventListener('click', (e)=>{
      const id = Number(e.currentTarget.dataset.id);
      addToCart(id);
    });
  });
}

function addToCart(id){
  const prod = products.find(p=>p.id===id);
  const found = cart.find(item=>item.id===id);
  if(found) found.qty += 1;
  else cart.push({id:prod.id, name:prod.name, price:prod.price, qty:1});
  renderCart();
}

function renderCart(){
  cartEl.innerHTML = '';
  if(cart.length===0){ cartEl.innerText = 'Порожня'; totalEl.innerText=''; return;}
  cart.forEach(item=>{
    const div = document.createElement('div');
    div.innerText = `${item.name} x${item.qty} — ${item.price * item.qty} грн`;
    cartEl.appendChild(div);
  });
  const total = cart.reduce((s,it)=>s + it.price*it.qty, 0);
  totalEl.innerText = `Сума: ${total} грн`;
}

checkoutBtn.addEventListener('click', ()=>{
  if(cart.length===0){ alert('Кошик порожній'); return; }
  modal.classList.remove('hidden');
});
closeModal.addEventListener('click', ()=> modal.classList.add('hidden'));

sendOrderBtn.addEventListener('click', ()=>{
  const name = document.getElementById('name').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const address = document.getElementById('address').value.trim();
  const comment = document.getElementById('comment').value.trim();
  if(!name || !phone){ alert('Вкажіть імя та телефон'); return}
  const payload = {
    name, phone, address, comment,
    cart: cart.map(c=>({name:c.name, price:c.price, qty:c.qty}))
  };
  // Send data back to the bot
  tg.sendData(JSON.stringify(payload));
  // Optionally close the WebApp
  tg.close();
});

// Initialize
renderCatalog();
renderCart();
