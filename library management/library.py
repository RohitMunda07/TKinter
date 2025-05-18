import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import json

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Modern Library Management System")
        self.root.geometry("1200x700")
        
        # Set theme colors
        self.colors = {
            "primary": "#3F51B5",  # Deep blue
            "secondary": "#4DB6AC",  # Teal
            "accent": "#FF7043",    # Coral
            "light_bg": "#F5F5F5",  # Light gray
            "dark_bg": "#263238",   # Dark blue-gray
            "text_light": "#FFFFFF", # White
            "text_dark": "#212121",  # Almost black
            "available": "#4CAF50", # Green
            "borrowed": "#FF5722"   # Orange-red
        }
        
        # Initialize data
        self.load_data()
        
        # Create UI
        self.setup_ui()
        
    def load_data(self):
        """Load books data from file or use default data"""
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                self.books_data = data.get("books", [])
                self.borrowed_books = data.get("borrowed", [])
        except (FileNotFoundError, json.JSONDecodeError):
            # Sample books data as fallback
            self.books_data = [
                {"id": 1, "name": "The Great Gatsby", "author": "F. Scott Fitzgerald", "status": "available", "category": "Fiction"},
                {"id": 2, "name": "To Kill a Mockingbird", "author": "Harper Lee", "status": "available", "category": "Fiction"},
                {"id": 3, "name": "1984", "author": "George Orwell", "status": "available", "category": "Sci-Fi"},
                {"id": 4, "name": "The Hobbit", "author": "J.R.R. Tolkien", "status": "available", "category": "Fantasy"},
                {"id": 5, "name": "Pride and Prejudice", "author": "Jane Austen", "status": "available", "category": "Romance"},
                {"id": 6, "name": "Harry Potter", "author": "J.K. Rowling", "status": "available", "category": "Fantasy"},
                {"id": 7, "name": "The Lord of the Rings", "author": "J.R.R. Tolkien", "status": "available", "category": "Fantasy"},
                {"id": 8, "name": "The Catcher in the Rye", "author": "J.D. Salinger", "status": "available", "category": "Fiction"}
            ]
            self.borrowed_books = []
    
    def save_data(self):
        """Save books data to file"""
        data = {
            "books": self.books_data,
            "borrowed": self.borrowed_books
        }
        with open("library_data.json", "w") as file:
            json.dump(data, file, indent=4)
    
    def setup_ui(self):
        """Create the main UI elements"""
        self.root.configure(bg=self.colors["light_bg"])
        
        # Create main frames
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Load initial data
        self.display_all_books()
        self.update_borrowed_list()
    
    def create_header(self):
        """Create the header with title and search bar"""
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], padx=15, pady=10)
        header_frame.pack(fill="x")
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg=self.colors["primary"])
        title_frame.pack(pady=(5, 15))
        
        tk.Label(title_frame, text="📚", font=("Segoe UI", 24), bg=self.colors["primary"], fg=self.colors["text_light"]).pack(side="left")
        tk.Label(title_frame, text="Library Management System", font=("Segoe UI", 24, "bold"), bg=self.colors["primary"], fg=self.colors["text_light"]).pack(side="left", padx=10)
        
        # Search bar
        search_frame = tk.Frame(header_frame, bg=self.colors["primary"])
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Style for the search frame
        search_container = tk.Frame(search_frame, bg=self.colors["text_light"], padx=2, pady=2, borderwidth=0)
        search_container.pack(anchor="center")
        
        # Search icon and entry
        search_icon_label = tk.Label(search_container, text="🔍", font=("Segoe UI", 12), bg=self.colors["text_light"])
        search_icon_label.pack(side="left", padx=(10, 0))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode, sv=self.search_var: self.on_search_change(sv))
        
        self.search_entry = tk.Entry(search_container, textvariable=self.search_var, width=50, font=("Segoe UI", 12), 
                                   relief="flat", bg=self.colors["text_light"], fg=self.colors["text_dark"])
        self.search_entry.pack(side="left", padx=5, ipady=8)
        
        # Add clear button
        clear_button = tk.Button(search_container, text="✕", font=("Segoe UI", 10), bg=self.colors["text_light"], 
                               fg=self.colors["text_dark"], borderwidth=0, command=self.clear_search)
        clear_button.pack(side="left", padx=(0, 10))
        
        # Category filter dropdown
        filter_frame = tk.Frame(header_frame, bg=self.colors["primary"])
        filter_frame.pack(pady=(0, 5))
        
        tk.Label(filter_frame, text="Filter by:", font=("Segoe UI", 10), bg=self.colors["primary"], fg=self.colors["text_light"]).pack(side="left", padx=(0, 5))
        
        categories = ["All"] + sorted(list(set(book["category"] for book in self.books_data)))
        self.category_var = tk.StringVar(value="All")
        
        category_menu = ttk.Combobox(filter_frame, textvariable=self.category_var, values=categories, state="readonly", width=15)
        category_menu.pack(side="left")
        category_menu.bind("<<ComboboxSelected>>", lambda e: self.filter_books())
        
        # Status filter
        tk.Label(filter_frame, text="Status:", font=("Segoe UI", 10), bg=self.colors["primary"], fg=self.colors["text_light"]).pack(side="left", padx=(20, 5))
        
        self.status_var = tk.StringVar(value="All")
        status_menu = ttk.Combobox(filter_frame, textvariable=self.status_var, values=["All", "Available", "Borrowed"], state="readonly", width=15)
        status_menu.pack(side="left")
        status_menu.bind("<<ComboboxSelected>>", lambda e: self.filter_books())
    
    def create_main_content(self):
        """Create the main content area with books display and borrowed books panel"""
        # Main content frame with Notebook
        self.content_frame = ttk.Notebook(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Books tab
        self.books_tab = tk.Frame(self.content_frame, bg=self.colors["light_bg"])
        self.content_frame.add(self.books_tab, text="Books Collection")
        
        # Split the books tab into books area and borrowed books area
        self.books_container = tk.PanedWindow(self.books_tab, orient=tk.HORIZONTAL, sashwidth=4, bg=self.colors["light_bg"])
        self.books_container.pack(fill="both", expand=True)
        
        # Create books frame with a canvas for scrolling
        books_outer_frame = tk.Frame(self.books_container, bg=self.colors["light_bg"])
        
        # Create a canvas with scrollbar
        self.books_canvas = tk.Canvas(books_outer_frame, bg=self.colors["light_bg"])
        scrollbar = ttk.Scrollbar(books_outer_frame, orient="vertical", command=self.books_canvas.yview)
        self.books_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.books_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas for the books
        self.books_frame = tk.Frame(self.books_canvas, bg=self.colors["light_bg"])
        self.books_canvas_window = self.books_canvas.create_window((0, 0), window=self.books_frame, anchor="nw")
        
        # Configure the canvas to adjust with resizing
        self.books_frame.bind("<Configure>", self.on_books_frame_configure)
        self.books_canvas.bind("<Configure>", self.on_books_canvas_configure)
        self.books_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Create the borrowed books frame
        borrowed_outer_frame = tk.Frame(self.books_container, bg=self.colors["light_bg"], width=300)
        borrowed_title_frame = tk.Frame(borrowed_outer_frame, bg=self.colors["secondary"], padx=10, pady=5)
        borrowed_title_frame.pack(fill="x")
        
        tk.Label(borrowed_title_frame, text="Borrowed Books", font=("Segoe UI", 14, "bold"), 
                bg=self.colors["secondary"], fg=self.colors["text_light"]).pack(anchor="w")
        
        # Borrowed books scrollable area
        borrowed_scroll_frame = tk.Frame(borrowed_outer_frame, bg=self.colors["light_bg"])
        borrowed_scroll_frame.pack(fill="both", expand=True)
        
        self.borrowed_canvas = tk.Canvas(borrowed_scroll_frame, bg=self.colors["light_bg"])
        borrowed_scrollbar = ttk.Scrollbar(borrowed_scroll_frame, orient="vertical", command=self.borrowed_canvas.yview)
        self.borrowed_canvas.configure(yscrollcommand=borrowed_scrollbar.set)
        
        borrowed_scrollbar.pack(side="right", fill="y")
        self.borrowed_canvas.pack(side="left", fill="both", expand=True)
        
        self.borrowed_frame = tk.Frame(self.borrowed_canvas, bg=self.colors["light_bg"])
        self.borrowed_canvas_window = self.borrowed_canvas.create_window((0, 0), window=self.borrowed_frame, anchor="nw")
        
        self.borrowed_frame.bind("<Configure>", lambda e: self.borrowed_canvas.configure(scrollregion=self.borrowed_canvas.bbox("all")))
        
        # Add empty label for spacing
        tk.Label(self.borrowed_frame, text="", bg=self.colors["light_bg"]).pack()
        
        # Add to paned window
        self.books_container.add(books_outer_frame)
        self.books_container.add(borrowed_outer_frame)
        self.books_container.paneconfigure(borrowed_outer_frame, minsize=300)
        
        # Management tab
        self.manage_tab = tk.Frame(self.content_frame, bg=self.colors["light_bg"])
        self.content_frame.add(self.manage_tab, text="Manage Library")
        
        # Set up the management tab
        self.setup_management_tab()
    
    def setup_management_tab(self):
        """Set up the library management tab"""
        # Title
        tk.Label(self.manage_tab, text="Library Management", font=("Segoe UI", 16, "bold"), 
                bg=self.colors["light_bg"], fg=self.colors["text_dark"]).pack(pady=(20, 10))
        
        # Main content with two columns
        management_frame = tk.Frame(self.manage_tab, bg=self.colors["light_bg"])
        management_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left column - Add new book
        add_frame = tk.LabelFrame(management_frame, text="Add New Book", font=("Segoe UI", 12), 
                                bg=self.colors["light_bg"], fg=self.colors["primary"], padx=15, pady=15)
        add_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        fields = [
            ("Book Title:", "name_entry"),
            ("Author:", "author_entry"),
            ("Category:", "category_entry")
        ]
        
        for i, (label_text, attr_name) in enumerate(fields):
            field_frame = tk.Frame(add_frame, bg=self.colors["light_bg"])
            field_frame.pack(fill="x", pady=5)
            
            tk.Label(field_frame, text=label_text, font=("Segoe UI", 10), 
                   bg=self.colors["light_bg"], width=10, anchor="w").pack(side="left")
            
            entry = tk.Entry(field_frame, font=("Segoe UI", 10), width=30)
            entry.pack(side="left", padx=5, fill="x", expand=True)
            setattr(self, attr_name, entry)
        
        # Add image button
        img_frame = tk.Frame(add_frame, bg=self.colors["light_bg"])
        img_frame.pack(fill="x", pady=10)
        
        tk.Label(img_frame, text="Cover Image:", font=("Segoe UI", 10), 
               bg=self.colors["light_bg"], width=10, anchor="w").pack(side="left")
        
        self.image_path_var = tk.StringVar()
        img_entry = tk.Entry(img_frame, font=("Segoe UI", 10), width=20, textvariable=self.image_path_var)
        img_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_btn = tk.Button(img_frame, text="Browse", font=("Segoe UI", 9), 
                              bg=self.colors["primary"], fg=self.colors["text_light"],
                              command=self.browse_image)
        browse_btn.pack(side="left", padx=5)
        
        # Add book button
        add_btn = tk.Button(add_frame, text="Add Book", font=("Segoe UI", 12, "bold"), 
                          bg=self.colors["secondary"], fg=self.colors["text_light"],
                          padx=20, pady=5, command=self.add_new_book)
        add_btn.pack(pady=20)
        
        # Right column - Statistics
        stats_frame = tk.LabelFrame(management_frame, text="Library Statistics", font=("Segoe UI", 12), 
                                  bg=self.colors["light_bg"], fg=self.colors["primary"], padx=15, pady=15)
        stats_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Statistics content
        self.stats_labels = {}
        stats = [
            ("Total Books:", "total_books"),
            ("Available Books:", "available_books"),
            ("Borrowed Books:", "borrowed_books"),
            ("Overdue Books:", "overdue_books"),
            ("Most Popular Category:", "popular_category")
        ]
        
        for i, (label_text, key) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg=self.colors["light_bg"])
            stat_frame.pack(fill="x", pady=8)
            
            tk.Label(stat_frame, text=label_text, font=("Segoe UI", 11), 
                   bg=self.colors["light_bg"], anchor="w").pack(side="left")
            
            value_label = tk.Label(stat_frame, text="0", font=("Segoe UI", 11, "bold"), 
                                 bg=self.colors["light_bg"], fg=self.colors["primary"])
            value_label.pack(side="right")
            self.stats_labels[key] = value_label
        
        # Refresh stats button
        refresh_btn = tk.Button(stats_frame, text="Refresh Statistics", font=("Segoe UI", 11), 
                              bg=self.colors["primary"], fg=self.colors["text_light"],
                              command=self.update_statistics)
        refresh_btn.pack(pady=15)
        
        # Initialize statistics
        self.update_statistics()
    
    def create_footer(self):
        """Create the footer with status bar"""
        footer_frame = tk.Frame(self.root, bg=self.colors["dark_bg"], height=30)
        footer_frame.pack(fill="x", side="bottom")
        
        # Status message on the left
        self.status_label = tk.Label(footer_frame, text="Ready", font=("Segoe UI", 9), 
                                   bg=self.colors["dark_bg"], fg=self.colors["text_light"])
        self.status_label.pack(side="left", padx=10)
        
        # Current date/time on the right
        date_str = datetime.now().strftime("%d %b %Y, %H:%M")
        date_label = tk.Label(footer_frame, text=date_str, font=("Segoe UI", 9), 
                            bg=self.colors["dark_bg"], fg=self.colors["text_light"])
        date_label.pack(side="right", padx=10)
    
    def on_books_frame_configure(self, event):
        """Update the scrollregion when the books frame size changes"""
        self.books_canvas.configure(scrollregion=self.books_canvas.bbox("all"))
    
    def on_books_canvas_configure(self, event):
        """Resize the books frame width when the canvas size changes"""
        self.books_canvas.itemconfig(self.books_canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if self.books_canvas.winfo_containing(event.x_root, event.y_root) == self.books_canvas:
            self.books_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def clear_search(self):
        """Clear the search field"""
        self.search_entry.delete(0, tk.END)
        self.filter_books()
    
    def on_search_change(self, sv):
        """Respond to search field changes"""
        self.filter_books()
    
    def filter_books(self):
        """Filter books based on search query, category and status"""
        query = self.search_var.get().lower()
        category = self.category_var.get()
        status = self.status_var.get().lower()
        
        filtered_books = []
        for book in self.books_data:
            # Apply search filter
            search_match = (query == "" or 
                          query in book["name"].lower() or 
                          query in book["author"].lower())
            
            # Apply category filter
            category_match = (category == "All" or book["category"] == category)
            
            # Apply status filter
            status_match = (status == "all" or 
                          (status == "available" and book["status"] == "available") or 
                          (status == "borrowed" and book["status"] == "borrowed"))
            
            if search_match and category_match and status_match:
                filtered_books.append(book)
        
        self.display_all_books(filtered_books)
        
        # Update status message
        if len(filtered_books) == 0:
            self.status_label.config(text="No books match your search criteria")
        else:
            self.status_label.config(text=f"Found {len(filtered_books)} books")
    
    def browse_image(self):
        """Open file dialog to select a book cover image"""
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.gif")]
        filepath = filedialog.askopenfilename(title="Select Book Cover Image", filetypes=filetypes)
        if filepath:
            self.image_path_var.set(filepath)
    
    def add_new_book(self):
        """Add a new book to the library"""
        name = self.name_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        image_path = self.image_path_var.get().strip()
        
        # Validate input
        if not name or not author or not category:
            messagebox.showwarning("Missing Information", "Please fill in all required fields.")
            return
        
        # Create new book entry
        new_id = max([book.get("id", 0) for book in self.books_data], default=0) + 1
        new_book = {
            "id": new_id,
            "name": name,
            "author": author,
            "category": category,
            "status": "available"
        }
        
        # Handle image
        if image_path:
            # Create images directory if it doesn't exist
            if not os.path.exists("images"):
                os.makedirs("images")
            
            # Copy image to images folder with appropriate name
            try:
                image_filename = f"{name.lower().replace(' ', '').replace(',', '').replace('.', '')}.jpg"
                image_dest = os.path.join("images", image_filename)
                
                img = Image.open(image_path)
                img = img.resize((150, 200), Image.Resampling.LANCZOS)
                img.save(image_dest)
            except Exception as e:
                messagebox.showwarning("Image Error", f"Could not process image: {str(e)}")
        
        # Add book and update display
        self.books_data.append(new_book)
        self.save_data()
        self.display_all_books()
        self.update_statistics()
        
        # Clear fields
        self.name_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.image_path_var.set("")
        
        # Update status
        self.status_label.config(text=f"Added new book: {name}")
        
        # Update category dropdown
        categories = ["All"] + sorted(list(set(book["category"] for book in self.books_data)))
        ttk.Combobox(values=categories)
    
    def update_statistics(self):
        """Update the statistics labels"""
        total = len(self.books_data)
        available = sum(1 for book in self.books_data if book["status"] == "available")
        borrowed = sum(1 for book in self.books_data if book["status"] == "borrowed")
        
        # Calculate overdue books
        overdue = 0
        today = datetime.now()
        for book in self.borrowed_books:
            due_date = datetime.strptime(book["due_date"], "%d-%m-%Y")
            if due_date < today:
                overdue += 1
        
        # Find most popular category
        categories = {}
        for book in self.books_data:
            cat = book["category"]
            if cat in categories:
                categories[cat] += 1
            else:
                categories[cat] = 1
        
        popular_category = max(categories.items(), key=lambda x: x[1])[0] if categories else "None"
        
        # Update labels
        self.stats_labels["total_books"].config(text=str(total))
        self.stats_labels["available_books"].config(text=str(available))
        self.stats_labels["borrowed_books"].config(text=str(borrowed))
        self.stats_labels["overdue_books"].config(text=str(overdue))
        self.stats_labels["popular_category"].config(text=popular_category)
    
    def display_all_books(self, display_books=None):
        """Display all books in the books frame"""
        # Clear existing books
        for widget in self.books_frame.winfo_children():
            widget.destroy()
        
        books_to_display = display_books or self.books_data
        
        if not books_to_display:
            # Show no books message
            msg_frame = tk.Frame(self.books_frame, bg=self.colors["light_bg"], padx=20, pady=20)
            msg_frame.pack(fill="both", expand=True)
            
            tk.Label(msg_frame, text="No books found", font=("Segoe UI", 14, "italic"), 
                   bg=self.colors["light_bg"], fg="#888").pack(pady=50)
            return
        
        # Calculate how many books can fit in a row based on frame width
        # Default to 4 books per row, this will be dynamically adjusted on resize
        books_per_row = 4
        
        # Create a grid of book cards
        for i, book in enumerate(books_to_display):
            row, col = divmod(i, books_per_row)
            self.create_book_card(book, row, col)
    
    def create_book_card(self, book, row, col):
        """Create a card for a book"""
        # Create a frame for the book card with a subtle border and shadow effect
        card = tk.Frame(self.books_frame, bg=self.colors["text_light"], padx=10, pady=10, 
                      highlightbackground="#ddd", highlightthickness=1, bd=0)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Add cover image
        try:
            image_name = book['name'].lower().replace(' ', '').replace("'", "").replace(",", "").replace(".", "") + ".jpg"
            image_path = os.path.join("images", image_name)
            
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((150, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(card, image=photo, bg=self.colors["text_light"])
                img_label.image = photo  # Keep a reference to prevent garbage collection
                img_label.pack(pady=5)
            else:
                # Create a placeholder
                placeholder = tk.Frame(card, width=150, height=200, bg="#e0e0e0")
                placeholder.pack(pady=5)
                tk.Label(placeholder, text="📚", font=("Segoe UI", 36), bg="#e0e0e0").place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            # Create a placeholder on error
            placeholder = tk.Frame(card, width=150, height=200, bg="#e0e0e0")
            placeholder.pack(pady=5)
            tk.Label(placeholder, text="📚", font=("Segoe UI", 36), bg="#e0e0e0").place(relx=0.5, rely=0.5, anchor="center")
        
        # Book title with ellipsis for long titles
        title = book["name"]
        if len(title) > 20:
            title = title[:18] + "..."
        
        tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=self.colors["text_light"], 
               wraplength=150, justify="center").pack(pady=(5, 0))
        
        tk.Label(card, text=f"by {book['author']}", font=("Segoe UI", 10), 
               bg=self.colors["text_light"], fg="#555").pack()
        
        # Category label
        category_frame = tk.Frame(card, bg=self.colors["primary"], padx=5, pady=2)
        category_frame.pack(pady=5)
        tk.Label(category_frame, text=book["category"], font=("Segoe UI", 9), 
               bg=self.colors["primary"], fg=self.colors["text_light"]).pack()
        
        # Status label with appropriate color
        status_color = self.colors["available"] if book["status"] == "available" else self.colors["borrowed"]
        status_text = "Available" if book["status"] == "available" else "Borrowed"
        
        status_label = tk.Label(card, text=status_text, font=("Segoe UI", 10, "bold"), 
                              bg=status_color, fg=self.colors["text_light"], width=10)
        status_label.pack(pady=5)
        
        # Action button (borrow or view details)
        button_text = "Borrow Book" if book["status"] == "available" else "Details"
        button_color = self.colors["secondary"] if book["status"] == "available" else "#999"
        button_state = "normal" if book["status"] == "available" else "disabled"
        
        action_button = tk.Button(card, text=button_text, font=("Segoe UI", 10, "bold"), 
                                bg=button_color, fg=self.colors["text_light"], 
                                width=15, pady=5, bd=0,
                                state=button_state, 
                                command=lambda: self.borrow_book(book))
        action_button.pack(pady=8)
    
    def borrow_book(self, book):
        """Borrow a book and update records"""
        book_id = book["id"]
        
        # Find the book in the data
        for b in self.books_data:
            if b["id"] == book_id and b["status"] == "available":
                b["status"] = "borrowed"
                due_date = datetime.now() + timedelta(days=14)
                due_date_str = due_date.strftime("%d-%m-%Y")
                
                # Add to borrowed books list
                self.borrowed_books.append({
                    "id": book_id,
                    "name": b["name"],
                    "author": b["author"],
                    "due_date": due_date_str
                })
                
                # Save data and update UI
                self.save_data()
                self.update_borrowed_list()
                self.display_all_books()
                self.update_statistics()
                
                # Show success message
                messagebox.showinfo("Success", f"You have borrowed '{b['name']}'\nReturn by: {due_date_str}")
                self.status_label.config(text=f"Book '{b['name']}' borrowed successfully")
                return
                
        # If we get here, the book is not available
        messagebox.showinfo("Not Available", f"'{book['name']}' is not available for borrowing.")
    
    def return_book(self, index):
        """Return a borrowed book"""
        if 0 <= index < len(self.borrowed_books):
            book_id = self.borrowed_books[index]["id"]
            book_name = self.borrowed_books[index]["name"]
            
            # Update book status
            for book in self.books_data:
                if book["id"] == book_id:
                    book["status"] = "available"
                    break
            
            # Remove from borrowed list
            self.borrowed_books.pop(index)
            
            # Save data and update UI
            self.save_data()
            self.update_borrowed_list()
            self.display_all_books()
            self.update_statistics()
            
            # Show success message
            self.status_label.config(text=f"Book '{book_name}' returned successfully")
    
    def update_borrowed_list(self):
        """Update the borrowed books list display"""
        # Clear existing content
        for widget in self.borrowed_frame.winfo_children():
            widget.destroy()
        
        if not self.borrowed_books:
            # Show empty message
            empty_label = tk.Label(self.borrowed_frame, text="No borrowed books", 
                                 font=("Segoe UI", 11, "italic"), bg=self.colors["light_bg"], fg="#888")
            empty_label.pack(pady=20, padx=10)
        else:
            today = datetime.now()
            
            # Add each borrowed book
            for i, book in enumerate(self.borrowed_books):
                # Calculate if overdue
                due_date = datetime.strptime(book["due_date"], "%d-%m-%Y")
                is_overdue = due_date < today
                
                # Create card with different color if overdue
                bg_color = "#fff4f4" if is_overdue else self.colors["text_light"]
                border_color = self.colors["borrowed"] if is_overdue else "#ddd"
                
                item_frame = tk.Frame(self.borrowed_frame, bg=bg_color, padx=10, pady=10,
                                    highlightbackground=border_color, highlightthickness=1)
                item_frame.pack(fill="x", padx=10, pady=5)
                
                # Book info
                info_frame = tk.Frame(item_frame, bg=bg_color)
                info_frame.pack(fill="x")
                
                tk.Label(info_frame, text=book["name"], font=("Segoe UI", 12, "bold"), 
                       bg=bg_color, wraplength=200, anchor="w").pack(fill="x")
                
                tk.Label(info_frame, text=f"by {book['author']}", font=("Segoe UI", 10), 
                       bg=bg_color, fg="#555").pack(anchor="w")
                
                # Due date with warning if overdue
                date_frame = tk.Frame(item_frame, bg=bg_color)
                date_frame.pack(fill="x", pady=(5, 0))
                
                date_text = f"Due: {book['due_date']}"
                date_color = "red" if is_overdue else "#555"
                date_font = ("Segoe UI", 10, "bold") if is_overdue else ("Segoe UI", 10)
                
                tk.Label(date_frame, text=date_text, font=date_font, bg=bg_color, fg=date_color).pack(side="left")
                
                if is_overdue:
                    overdue_days = (today - due_date).days
                    tk.Label(date_frame, text=f"({overdue_days} days overdue)", 
                           font=("Segoe UI", 9), bg=bg_color, fg="red").pack(side="left", padx=5)
                
                # Return button
                button_frame = tk.Frame(item_frame, bg=bg_color)
                button_frame.pack(fill="x", pady=(8, 0))
                
                return_btn = tk.Button(button_frame, text="Return Book", font=("Segoe UI", 10), 
                                      bg=self.colors["secondary"], fg=self.colors["text_light"],
                                      command=lambda idx=i: self.return_book(idx))
                return_btn.pack(side="right")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()