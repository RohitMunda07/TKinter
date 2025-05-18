import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

# Sample menu data
menu_items = [
    {"name": "Burger", "price": 120, "category": "Snacks"},
    {"name": "Cake", "price": 150, "category": "Dessert"},
    {"name": "Pasta", "price": 100, "category": "Meals"},
    {"name": "Coffee", "price": 80, "category": "Drinks"},
    {"name": "Tea", "price": 30, "category": "Drinks"},
    {"name": "Fires", "price": 60, "category": "Snacks"},
    {"name": "Chocolate Ice Cream", "price": 90, "category": "Dessert"},
    {"name": "Coca Cola", "price": 40, "category": "Drinks"},
    {"name": "Cup Cake", "price": 60, "category": "Dessert"},
    {"name": "Desert", "price": 110, "category": "Dessert"},
    {"name": "Fruit Salad", "price": 70, "category": "Healthy"},
    {"name": "Large Sandwich", "price": 130, "category": "Meals"},
    {"name": "Milkshake", "price": 80, "category": "Drinks"},
    {"name": "Noodles", "price": 90, "category": "Meals"},
    {"name": "Pancake", "price": 100, "category": "Dessert"},
    {"name": "Roll", "price": 60, "category": "Snacks"},
    {"name": "Sandwich", "price": 90, "category": "Meals"},
    {"name": "Slice", "price": 50, "category": "Dessert"},
]

cart = []

def add_to_cart(item):
    cart.append(item)
    update_cart()

def remove_from_cart(index):
    if 0 <= index < len(cart):
        del cart[index]
        update_cart()

def update_cart():
    for widget in cart_items_frame.winfo_children():
        widget.destroy()

    total = 0
    if not cart:
        empty_label = tk.Label(cart_items_frame, text="Your cart is empty", font=("Segoe UI", 10, "italic"), bg="#fdfdfd", fg="#888")
        empty_label.pack(pady=20)
    else:
        for i, food in enumerate(cart):
            item_frame = tk.Frame(cart_items_frame, bg="#f5f5f5", padx=5, pady=5, highlightbackground="#ddd", highlightthickness=1)
            item_frame.pack(fill="x", pady=2)

            tk.Label(item_frame, text=food['name'], font=("Segoe UI", 10, "bold"), bg="#f5f5f5").pack(side="left", padx=5)
            tk.Label(item_frame, text=f"Rs.{food['price']}", font=("Segoe UI", 10), bg="#f5f5f5").pack(side="left", padx=10)
            tk.Button(item_frame, text="✕", font=("Segoe UI", 8), bg="#ff5722", fg="white", width=2, relief="flat", command=lambda idx=i: remove_from_cart(idx)).pack(side="right", padx=5)

            total += food['price']

    total_label.config(text=f"Total: Rs.{total}")

def search_food():
    query = search_entry.get().lower()
    filtered_menu = [item for item in menu_items if query in item['name'].lower()]
    display_all_food(filtered_menu)
    selected_category.set("All")

def filter_by_category():
    category = selected_category.get()
    if category == "All":
        display_all_food()
    else:
        filtered = [item for item in menu_items if item['category'] == category]
        display_all_food(filtered)

def display_all_food(display_menu=None):
    if display_menu is None:
        display_menu = menu_items

    for widget in food_frame.winfo_children():
        widget.destroy()

    columns = 6
    for index, item in enumerate(display_menu):
        row = index // columns
        col = index % columns
        create_food_card(item, row, col)

def create_food_card(item, row, col):
    card = tk.Frame(food_frame, width=180, height=250, bd=0, bg="#f5f5f5", padx=10, pady=10, highlightbackground="#ccc", highlightthickness=1)
    card.grid_propagate(False)
    card.grid(row=row, column=col, padx=15, pady=15)

    try:
        image_name = item['name'].lower().replace(' ', '') + ".jpg"
        image_path = os.path.join("images", image_name)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        img = Image.open(image_path)
        img = img.resize((160, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(card, image=photo, bg="#f5f5f5")
        img_label.image = photo
        img_label.pack()
    except Exception as e:
        print("Image load error:", e)
        img_label = tk.Label(card, text="[No Image]", bg="#ccc", width=15, height=7, font=("Segoe UI", 10))
        img_label.pack()

    tk.Label(card, text=item['name'], font=("Segoe UI", 12, "bold"), bg="#f5f5f5", wraplength=150, justify="center").pack(pady=(5, 0))
    tk.Label(card, text=f"Rs. {item['price']}", font=("Segoe UI", 10), bg="#f5f5f5").pack()
    tk.Button(card, text="Add to Cart", font=("Segoe UI", 10), bg="#4CAF50", fg="white", activebackground="#45a049", command=lambda: add_to_cart(item)).pack(pady=8)

def place_order():
    if not cart:
        messagebox.showwarning("Empty Cart", "Please add items to the cart.")
    else:
        messagebox.showinfo("Order Placed", "Thank you! Your food is on the way 🚚")
        cart.clear()
        update_cart()

root = tk.Tk()
root.title("🍔 Online Food Ordering App")
root.geometry("980x620")
root.configure(bg="white")

search_frame = tk.Frame(root, bg="white")
search_frame.pack(pady=15)

search_entry = tk.Entry(search_frame, width=40, font=("Segoe UI", 12), bg="#ddd", relief="flat", insertbackground="black")
search_entry.pack(side="left", padx=5, ipady=5)

search_btn = tk.Button(search_frame, text="🔍", command=search_food, bg="#4CAF50", fg="white", font=("Segoe UI", 12), relief="flat", cursor="hand2", padx=10)
search_btn.pack(side="left", padx=5)

categories = ["All"] + sorted(set(item["category"] for item in menu_items))
selected_category = tk.StringVar(value="All")

category_menu = tk.OptionMenu(search_frame, selected_category, *categories, command=lambda _: filter_by_category())
category_menu.config(font=("Segoe UI", 11), bg="#eee", relief="flat")
category_menu.pack(side="left", padx=10)

food_container = tk.Frame(root, bg="white")
food_container.pack(side="left", fill="both", expand=True, padx=20, pady=10)

food_canvas = tk.Canvas(food_container, bg="white", highlightthickness=0)
food_scrollbar = tk.Scrollbar(food_container, orient="vertical", command=food_canvas.yview)
food_canvas.configure(yscrollcommand=food_scrollbar.set)

food_scrollbar.pack(side="right", fill="y")
food_canvas.pack(side="left", fill="both", expand=True)

food_frame = tk.Frame(food_canvas, bg="white")
food_window = food_canvas.create_window((0, 0), window=food_frame, anchor="nw")

def update_scrollregion(event):
    food_canvas.configure(scrollregion=food_canvas.bbox("all"))
food_frame.bind("<Configure>", update_scrollregion)

def resize_food_window(event):
    food_canvas.itemconfig(food_window, width=event.width)
food_canvas.bind("<Configure>", resize_food_window)

display_all_food()

cart_frame = tk.Frame(root, bd=0, padx=15, pady=15, bg="#fdfdfd", highlightbackground="#ccc", highlightthickness=1)
cart_frame.pack(side="right", fill="y", padx=10, pady=10)

cart_title = tk.Label(cart_frame, text="🛒 Your Cart", font=("Segoe UI", 14, "bold"), bg="#fdfdfd")
cart_title.pack(pady=(0, 10))

cart_canvas_frame = tk.Frame(cart_frame, bg="#fdfdfd")
cart_canvas_frame.pack(fill="both", expand=True)

cart_canvas = tk.Canvas(cart_canvas_frame, bg="#fdfdfd", highlightthickness=0)
cart_scrollbar = tk.Scrollbar(cart_canvas_frame, orient="vertical", command=cart_canvas.yview)
cart_scrollbar.pack(side="right", fill="y")
cart_canvas.pack(side="left", fill="both", expand=True)
cart_canvas.configure(yscrollcommand=cart_scrollbar.set)

cart_items_frame = tk.Frame(cart_canvas, bg="#fdfdfd")
cart_items_frame.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))
cart_canvas_window = cart_canvas.create_window((0, 0), window=cart_items_frame, anchor="nw")

def configure_cart_items_frame(event):
    cart_canvas.itemconfig(cart_canvas_window, width=event.width)
cart_canvas.bind("<Configure>", configure_cart_items_frame)

total_frame = tk.Frame(cart_frame, bg="#fdfdfd", pady=10)
total_frame.pack(fill="x")

total_label = tk.Label(total_frame, text="Total: Rs.0", font=("Segoe UI", 12, "bold"), bg="#fdfdfd")
total_label.pack(side="right")

order_btn = tk.Button(cart_frame, text="Order Now", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", cursor="hand2", padx=15, pady=5, activebackground="#45a049", command=place_order)
order_btn.pack(pady=10, fill="x")

root.mainloop()