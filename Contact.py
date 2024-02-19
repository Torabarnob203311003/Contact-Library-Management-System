import re
import os
import json

class Contact:
    def __init__(self, name, email, phone_number):
        self.name = name
        self.set_email(email)
        self.set_phone_number(phone_number)

    def set_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")
        self.email = email

    def set_phone_number(self, phone_number):
        phone_pattern = re.compile(r'^\d{3}-\d{8}$')
        if not phone_pattern.match(phone_number):
            raise ValueError("Invalid phone number format")
        self.phone_number = phone_number

def read_contacts():
    contacts = []
    if os.path.exists('contacts.json'):
        with open('contacts.json', 'r') as file:
            contacts = json.load(file)
    return contacts

def write_contacts(contacts):
    with open('contacts.json', 'w') as file:
        json.dump(contacts, file)

def add_contact():
    name = input("Enter name: ")
    email = input("Enter email: ")
    phone_number = input("Enter phone number (format: 017-123456789): ")

    try:
        contact = Contact(name, email, phone_number)
        contacts = read_contacts()
        contacts.append({"name": contact.name, "email": contact.email, "phone_number": contact.phone_number})
        write_contacts(contacts)
        print("Contact added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Contact not added.")

def list_contacts():
    contacts = read_contacts()
    if not contacts:
        print("No contacts found.")
    else:
        for contact in contacts:
            print(f"Name: {contact['name']}, Email: {contact['email']}, Phone: {contact['phone_number']}")

def search_contact():
    name_to_search = input("Enter the name to search: ")
    contacts = read_contacts()
    found_contacts = [contact for contact in contacts if name_to_search.lower() in contact['name'].lower()]
    
    if not found_contacts:
        print("Contact not found.")
    else:
        for contact in found_contacts:
            print(f"Name: {contact['name']}, Email: {contact['email']}, Phone: {contact['phone_number']}")

def delete_contact():
    name_to_delete = input("Enter the name to delete: ")
    contacts = read_contacts()
    remaining_contacts = [contact for contact in contacts if name_to_delete.lower() not in contact['name'].lower()]

    if len(remaining_contacts) == len(contacts):
        print("Contact not found.")
    else:
        write_contacts(remaining_contacts)
        print("Contact deleted successfully.")

if __name__ == "__main__":
    while True:
        print("\n1. Add Contact\n2. List Contacts\n3. Search Contact\n4. Delete Contact\n5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_contact()
        elif choice == '2':
            list_contacts()
        elif choice == '3':
            search_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")