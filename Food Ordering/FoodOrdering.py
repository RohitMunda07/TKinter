import tkinter as tk
from tkinter import messagebox

# Sample menu data
menu = [
    {"name": "Burger", "price": 120},
    {"name": "Pizza", "price": 250},
    {"name": "Pasta", "price": 180},
    {"name": "Fries", "price": 90}
]

cart = []

def add_to_cart(item):
    cart.append(item)
    update_cart()

def update_cart():
    cart_list.delete(0, tk.END)
    total = 0
    for food in cart:
        cart_list.insert(tk.END, f"{food['name']} -------- Rs.{food['price']}")
        total += food['price']
    cart_list.insert(tk.END, "-" * 40)
    cart_list.insert(tk.END, f"Total{' ' * 21}Rs.{total}")

def search_food():
    query = search_entry.get().lower()
    for widget in food_frame.winfo_children():
        widget.destroy()
    for item in menu:
        if query in item['name'].lower():
            create_food_card(item)

def create_food_card(item):
    card = tk.Frame(food_frame, bd=0, bg="#f5f5f5", padx=10, pady=10, highlightbackground="#ccc", highlightthickness=1)
    card.pack(side="left", padx=15, pady=15)

    img_placeholder = tk.Label(card, text="[Image]", bg="#ccc", width=15, height=7, font=("Segoe UI", 10))
    img_placeholder.pack()

    name_label = tk.Label(card, text=item["name"], font=("Segoe UI", 12, "bold"), bg="#f5f5f5")
    name_label.pack(pady=(5, 0))

    price_label = tk.Label(card, text=f"Rs. {item['price']}", font=("Segoe UI", 10), bg="#f5f5f5")
    price_label.pack()

    add_btn = tk.Button(card, text="Add to Cart", font=("Segoe UI", 10), bg="#4CAF50", fg="white", activebackground="#45a049", relief="flat", cursor="hand2", command=lambda: add_to_cart(item))
    add_btn.pack(pady=8)

def place_order():
    if not cart:
        messagebox.showwarning("Empty Cart", "Please add items to the cart.")
    else:
        messagebox.showinfo("Order Placed", "Thank you! Your food is on the way 🚚")
        cart.clear()
        update_cart()

# Main window setup
root = tk.Tk()
root.title("🍔 Online Food Ordering App")
root.geometry("950x600")
root.configure(bg="white")

# Search bar
search_frame = tk.Frame(root, bg="white")
search_frame.pack(pady=15)

search_entry = tk.Entry(search_frame, width=40, font=("Segoe UI", 12), bg="#ddd", relief="flat", insertbackground="black")
search_entry.pack(side="left", padx=5, ipady=5)

search_btn = tk.Button(search_frame, text="🔍", command=search_food, bg="#4CAF50", fg="white", font=("Segoe UI", 12), relief="flat", cursor="hand2", padx=10)
search_btn.pack(side="left")

# Food display area
food_frame = tk.Frame(root, bg="white")
food_frame.pack(side="left", padx=20, pady=10)

for item in menu:
    create_food_card(item)

# Cart area
cart_frame = tk.Frame(root, bd=0, padx=15, pady=15, bg="#fdfdfd", highlightbackground="#ccc", highlightthickness=1)
cart_frame.pack(side="right", fill="y", padx=10, pady=10)

cart_title = tk.Label(cart_frame, text="🛒 Your Cart", font=("Segoe UI", 14, "bold"), bg="#fdfdfd")
cart_title.pack(pady=(0, 10))

cart_list = tk.Listbox(cart_frame, width=40, height=20, font=("Courier New", 10), bg="#f0f0f0", bd=0)
cart_list.pack()

order_btn = tk.Button(cart_frame, text="Order Now", font=("Segoe UI", 12, "bold"), bg="#ff5722", fg="white", relief="flat", cursor="hand2", padx=15, pady=5, activebackground="#e64a19")
order_btn.config(command=place_order)
order_btn.pack(pady=15)

root.mainloop()
