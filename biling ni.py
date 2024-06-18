import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
import csv
from tkinter import filedialog


import os

class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1200x700")
        self.root.configure(bg="#e0f7fa")
        self.on_login_success = on_login_success

        self.setup_ui()

    def setup_ui(self):
        self.login_frame = tk.Frame(self.root, bg="#e0f7fa")
        self.login_frame.pack(expand=True)

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 14), bg="#e0f7fa")
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.login_frame, font=("Arial", 14))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 14), bg="#e0f7fa")
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.check_credentials, font=("Arial", 14), bg="#0288d1", fg="#ffffff")
        self.login_button.pack(pady=20)

    def read_credentials_from_csv(self, filename):
        credentials = {}
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    credentials[row[0]] = row[1]
        return credentials

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        credentials = self.read_credentials_from_csv("admin.csv")

        if username in credentials and credentials[username] == password:
            self.on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class BillingSystem:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Billing System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#e0f7fa")

        self.username = username

        self.items = {}
        self.total_amount = 0

        # Predefined items with prices in Indonesian Rupiah
        self.available_items = {
            "Nasi Goreng": {"price": 20000, "image": "ng.png"},
            "Mie Goreng": {"price": 18000, "image": "mg.png"},
            "Sate Ayam": {"price": 25000, "image": "sate.png"},
            "Ayam Goreng": {"price": 30000, "image": "ag.png"},
            "Bakso": {"price": 15000, "image": "b.png"},
            # Tambahkan lebih banyak item jika diperlukan
        }

        self.setup_ui()

    def setup_ui(self):
        # Header Frame
        self.header_frame = tk.Frame(self.root, bg="#0288d1", height=100)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        # Load and display logo in header
        self.logo = Image.open("logo.png")
        self.logo = self.logo.resize((80, 80), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self.header_frame, image=self.logo_img, bg="#0288d1")
        self.logo_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.header_label = tk.Label(self.header_frame, text="Billing System", font=("Arial", 24, "bold"), bg="#0288d1", fg="#ffffff")
        self.header_label.pack(side=tk.LEFT, pady=10)
        
        # Log out button
        self.btn_logout = tk.Button(self.header_frame, text="Log Out", command=self.log_out, bg="#e57373", fg="#ffffff", font=("Arial", 12, "bold"))
        self.btn_logout.pack(side=tk.RIGHT, padx=10, pady=10)

        # Logged in information
        self.logged_in_label = tk.Label(self.header_frame, text=f"Logged in as: {self.username}", font=("Arial", 12), bg="#0288d1", fg="#ffffff")
        self.logged_in_label.pack(side=tk.RIGHT, padx=20, pady=10)

        # Current date and time
        self.date_time_label = tk.Label(self.header_frame, text="", font=("Arial", 12), bg="#0288d1", fg="#ffffff")
        self.date_time_label.pack(side=tk.RIGHT, padx= 10, pady=10)
        self.update_date_time()  # Start updating date and time

        # Main Content Frame
        self.content_frame = tk.Frame(self.root, bg="#e0f7fa")
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Left Frame with scrollable items
        self.left_frame = tk.Frame(self.content_frame, bg="#e0f7fa", width=800)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a Canvas to enable scrolling
        self.canvas = tk.Canvas(self.left_frame, bg="#e0f7fa")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a Scrollbar to the Canvas
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Creating a Frame inside the Canvas to hold item widgets
        self.item_frame = tk.Frame(self.canvas, bg="#e0f7fa")
        self.canvas.create_window((0, 0), window=self.item_frame, anchor="nw")

        self.populate_items()

        # Right Frame for order details
        self.right_frame = tk.Frame(self.content_frame, bg="#e0f7fa", width=400)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Order details in right frame
        columns = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings', height=15)
        self.tree.heading('#1', text='Item Name')
        self.tree.heading('#2', text='Quantity')
        self.tree.heading('#3', text='Price')
        self.tree.column('#1', anchor=tk.CENTER, width=150)
        self.tree.column('#2', anchor=tk.CENTER, width=100)
        self.tree.column('#3', anchor=tk.CENTER, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Footer for total display
        self.footer_frame = tk.Frame(self.right_frame, bg="#e0f7fa")
        self.footer_frame.pack(fill=tk.BOTH, pady=10, padx=10)

        self.lbl_total = tk.Label(self.footer_frame, text="Total: Rp 0.00", font=("Arial", 14, "bold"), bg="#e0f7fa")
        self.lbl_total.pack(side=tk.RIGHT)

        self.btn_order = tk.Button(self.footer_frame, text="Order", command=self.generate_invoice, bg="#ffeb3b", fg="#000000", font=("Arial", 12, "bold"))
        self.btn_order.pack(side=tk.LEFT, padx=10)

        self.btn_cancel = tk.Button(self.footer_frame, text="Cancel", command=self.reset_form, bg="#e57373", fg="#ffffff", font=("Arial", 12, "bold"))
        self.btn_cancel.pack(side=tk.LEFT, padx=10)

    def populate_items(self):
        # Create buttons for each item
        self.item_buttons = {}
        for item_name, item_info in self.available_items.items():
            item_frame = tk.Frame(self.item_frame, bg="#ffffff", bd=2, relief=tk.RAISED, padx=5, pady=5)
            item_frame.pack(pady=5, padx=10, fill=tk.X)

            item_image = Image.open(item_info["image"])
            item_image = item_image.resize((100, 100), Image.LANCZOS)
            item_image = ImageTk.PhotoImage(item_image)

            item_label = tk.Label(item_frame, image=item_image, bg="#ffffff")
            item_label.image = item_image  # Keep a reference to avoid garbage collection
            item_label.pack(side=tk.LEFT)

            item_name_label = tk.Label(item_frame, text=item_name, font=("Arial", 16, "bold"), bg="#ffffff")
            item_name_label.pack(side=tk.LEFT, padx=10)

            item_price_label = tk.Label(item_frame, text=f"Rp {item_info['price']:,}", font=("Arial", 14), bg="#ffffff")
            item_price_label.pack(side=tk.LEFT)

            item_button_add = tk.Button(item_frame, text="Add", command=lambda name=item_name: self.add_item(name))
            item_button_add.pack(side=tk.RIGHT, padx=5)

            item_button_remove = tk.Button(item_frame, text="Remove", command=lambda name=item_name: self.remove_item(name))
            item_button_remove.pack(side=tk.RIGHT, padx=5)

            # Bind double click event to enlarge the image
            item_label.bind("<Double-Button-1>", lambda event, img=item_image: self.enlarge_image(img))

            self.item_buttons[item_name] = (item_button_add, item_button_remove)

    def enlarge_image(self, image):
        enlarge_window = tk.Toplevel(self.root)
        enlarge_window.title("Enlarged Image")
        enlarged_label = tk.Label(enlarge_window, image=image)
        enlarged_label.pack()

    def add_item(self, item_name):
        if item_name in self.items:
            # If item already exists in the order, increment its quantity by 1
            self.items[item_name]['quantity'] += 1
            self.tree.item(item_name, values=(item_name, self.items[item_name]['quantity'], self.items[item_name]['price'] * self.items[item_name]['quantity']))
        else:
            # If item does not exist in the order, add it with quantity 1
            self.items[item_name] = {'quantity': 1, 'price': self.available_items[item_name]['price']}
            self.tree.insert('', tk.END, iid=item_name, values=(item_name, 1, self.available_items[item_name]['price']))
        self.update_total()

    def remove_item(self, item_name):
        if item_name in self.items:
            # If item quantity > 1, decrement its quantity by 1
            if self.items[item_name]['quantity'] > 1:
                self.items[item_name]['quantity'] -= 1
                self.tree.item(item_name, values=(item_name, self.items[item_name]['quantity'], self.items[item_name]['price'] * self.items[item_name]['quantity']))
            else:
                # If item quantity is 1, remove it from the order
                del self.items[item_name]
                self.tree.delete(item_name)
            self.update_total()

    def update_total(self):
        self.total_amount = sum(item_info['price'] * item_info['quantity'] for item_info in self.items.values())
        self.lbl_total.config(text=f"Total: Rp {self.total_amount:,.2f}")

    def reset_form(self):
        self.items = {}
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_total()

    def generate_invoice_id(self):
        current_date = datetime.now().strftime("%Y%m%d")
        if not hasattr(self, 'invoice_counter'):
            self.invoice_counter = 0
        else:
            self.invoice_counter += 1
        invoice_id = f"{current_date}-{self.invoice_counter}"
        return invoice_id

    def generate_invoice(self):
        if not self.items:
            messagebox.showerror("Error", "No items added to the order.")
            return
        
        order_id = self.generate_invoice_id()

        invoice_filename = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")],initialfile=f"invoice_{order_id}.txt",initialdir=os.getcwd(),title="Save Invoice As")

        if not invoice_filename:
            return
        
        with open(invoice_filename, "w") as invoice_file:
            invoice_file.write(f"Invoice ID: {order_id}\n")
            invoice_file.write(f"Admin: {self.username}\n")
            invoice_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            invoice_file.write("\nItems:\n")
            for item_name, details in self.items.items():
                invoice_file.write(f"{item_name} x{details['quantity']} - Rp {details['price'] * details['quantity']:,}\n")
            invoice_file.write(f"\nTotal: Rp {self.total_amount:,}\n")

        self.save_order_to_csv(order_id)
        messagebox.showinfo("Success", f"Invoice {order_id} generated and saved successfully.")
        self.reset_form()

    def display_invoice(self, invoice_text):
        invoice_window = tk.Toplevel(self.root)
        invoice_window.title("Invoice")
        invoice_window.geometry("400x600")
        text_invoice = tk.Text(invoice_window, wrap='word')
        text_invoice.pack(fill=tk.BOTH, expand=True)
        text_invoice.insert(tk.END, invoice_text)

        btn_close = ttk.Button(invoice_window, text="Close", command=invoice_window.destroy)
        btn_close.pack(side=tk.RIGHT, padx=10, pady=10)

    def update_date_time(self):
        # Get current date and time
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Update the label
        self.date_time_label.config(text=f"Date & Time: {formatted_datetime}")
        # Schedule the update every second
        self.date_time_label.after(1000, self.update_date_time)

    def log_out(self):
        # Destroy the current BillingSystem GUI
        self.root.destroy()
        
        # Re-create the login page
        root = tk.Tk()
        login_page = LoginPage(root, start_billing_system)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()

    def start_billing_system(username):
        # Destroy login window
        login_page.login_frame.destroy()
        # Start the billing system
        app = BillingSystem(root, username)

    login_page = LoginPage(root, start_billing_system)
    root.mainloop()

