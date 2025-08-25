import tkinter as tk
from tkinter import ttk, messagebox
import json, os

CONTACTS_FILE = "contacts.json"

# ------- File Handling --------
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "r") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# -------- Main Application --------
class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Modern Contact Book")
        self.root.geometry("500x600")
        self.root.config(bg="#f0f4f7")

        self.contacts = load_contacts()
        self.editing_contact = None  

        style = ttk.Style()
        style.theme_use("clam")

        # Header
        header = tk.Label(root, text="📞 Contact Book", font=("Arial", 20, "bold"),
                          bg="#4CAF50", fg="white", pady=10)
        header.pack(fill="x")

        # --- Input Fields ---
        frame = tk.Frame(root, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Name (required):", bg="#f0f4f7", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Phone (required):", bg="#f0f4f7", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
        self.phone_entry = ttk.Entry(frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Email (optional):", bg="#f0f4f7", font=("Arial", 11)).grid(row=2, column=0, sticky="w")
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg="#f0f4f7")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ Add", command=self.add_contact).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="✏️ Edit", command=self.load_for_edit).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="💾 Save Edit", command=self.save_edit).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(btn_frame, text="🗑 Delete", command=self.delete_contact).grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(btn_frame, text="👁 View", command=self.view_contact).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="🧹 Clear", command=self.clear_fields).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="🚪 Exit", command=root.destroy).grid(row=1, column=2, padx=5, pady=5)

        # --- Search Above List ---
        search_frame = tk.Frame(root, bg="#d9edf7", bd=2, relief="groove")
        search_frame.pack(pady=5, fill="x")

        tk.Label(search_frame, text="🔍 Search by Name:", bg="#d9edf7", font=("Arial", 11)).pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_contacts).pack(side="left", padx=5)

        # --- Contact List ---
        self.contact_list = tk.Listbox(root, width=50, height=15, bg="#ffffff", fg="#333",
                                       font=("Arial", 11), selectbackground="#4CAF50", selectforeground="white")
        self.contact_list.pack(pady=10)

        self.load_listbox()

    # -------- Utilities --------
    def load_listbox(self, filtered_contacts=None):
        self.contact_list.delete(0, tk.END)
        names = filtered_contacts if filtered_contacts is not None else self.contacts.keys()
        for name in sorted(names):
            self.contact_list.insert(tk.END, name)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    # -------- CRUD --------
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("⚠️ Warning", "Name and Phone are required!")
            return

        self.contacts[name] = {"phone": phone, "email": email if email else "—"}
        save_contacts(self.contacts)
        self.load_listbox()
        self.clear_fields()
        messagebox.showinfo("✅ Success", f"Contact '{name}' added!")

    def load_for_edit(self):
        sel = self.contact_list.curselection()
        if not sel:
            messagebox.showwarning("⚠️ Warning", "Select a contact to edit")
            return
        name = self.contact_list.get(sel)
        info = self.contacts[name]
        self.clear_fields()
        self.name_entry.insert(0, name)
        self.phone_entry.insert(0, info["phone"])
        self.email_entry.insert(0, "" if info["email"] == "—" else info["email"])
        self.editing_contact = name

    def save_edit(self):
        if not self.editing_contact:
            messagebox.showwarning("⚠️ Warning", "No contact selected for editing")
            return

        new_name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not new_name or not phone:
            messagebox.showwarning("⚠️ Warning", "Name and Phone are required!")
            return

        if new_name != self.editing_contact and self.editing_contact in self.contacts:
            del self.contacts[self.editing_contact]

        self.contacts[new_name] = {"phone": phone, "email": email if email else "—"}
        save_contacts(self.contacts)
        self.load_listbox()
        self.clear_fields()
        messagebox.showinfo("✅ Updated", f"Contact '{new_name}' updated!")
        self.editing_contact = None

    def delete_contact(self):
        sel = self.contact_list.curselection()
        if not sel:
            messagebox.showwarning("⚠️ Warning", "Select a contact to delete")
            return
        name = self.contact_list.get(sel)
        del self.contacts[name]
        save_contacts(self.contacts)
        self.load_listbox()
        messagebox.showinfo("🗑 Deleted", f"Contact '{name}' deleted")

    def view_contact(self):
        sel = self.contact_list.curselection()
        if not sel:
            messagebox.showwarning("⚠️ Warning", "Select a contact to view")
            return
        name = self.contact_list.get(sel)
        info = self.contacts[name]
        messagebox.showinfo("📌 Contact Info",
                            f"Name: {name}\n"
                            f"Phone: {info['phone']}\n"
                            f"Email: {info['email']}")

    # -------- Search --------
    def search_contacts(self):
        q = self.search_entry.get().lower()
        filtered = [name for name in self.contacts if q in name.lower()]
        self.load_listbox(filtered)

# -------- Run App --------
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()

