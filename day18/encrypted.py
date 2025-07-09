from cryptography.fernet import Fernet
from datetime import datetime

# ---- Key Management ----

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

# ---- Note Functions ----

def write_note():
    note = input("Enter your note: ")
    key = load_key()
    f = Fernet(key)
    encrypted_note = f.encrypt(note.encode())

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("notes.txt", "ab") as file:
        file.write(f"{timestamp}||".encode() + encrypted_note + b"\n")
    print("✅ Note saved securely!")

def read_notes():
    key = load_key()
    f = Fernet(key)

    try:
        with open("notes.txt", "rb") as file:
            for line in file:
                timestamp, encrypted_note = line.split(b"||")
                decrypted_note = f.decrypt(encrypted_note.strip())
                print(f"[{timestamp.decode()}] {decrypted_note.decode()}")
    except FileNotFoundError:
        print("No notes found.")

# ---- CLI Menu ----

def menu():
    while True:
        print("\n🛡 Encrypted Notes CLI App")
        print("1. Write a new note")
        print("2. Read all notes")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            write_note()
        elif choice == '2':
            read_notes()
        elif choice == '3':
            print("Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# ---- Main ----

if __name__ == "__main__":
    # Uncomment the below line only once to generate the key
    #generate_key()
    menu()
