import sqlite3
import math
con = sqlite3.connect("inventory.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL
    )
""")
print("Welcome to the Inventory Management System")
def display_menu():
    print("\nMenu:")
    print("A - Add Item")
    print("V - View Items")
    print("S - Search Item")
    print("U - Update Item")
    print("D - Delete Item")
    print("E - Exit")
    print("C - Clear memory")
    
def add_item(name, price):
    if not name:
        return "Name cannot be empty"
    elif not math.isfinite(price) or price < 0:
        return "Price cannot be negative or infinite"
    cur.execute("""INSERT INTO inventory (name,price) VALUES(?,?)""",(name,price))
    con.commit()
    return "Item added successfully."
def view_items():
    cur.execute("""SELECT id,name,price FROM inventory """)
    print("Items in inventory:")
    items = cur.fetchall()
    if not items:
        print("No items in inventory.")
    else:
        for row in items:
            print(f"ID: {row[0]} - Name: {row[1]} - Price: {row[2]}")
def search_item(search_id):
    cur.execute("""SELECT id,name,price FROM inventory WHERE id = ?""",(search_id,))
    item = cur.fetchone()
    if item:
        print(f"ID: {item[0]} - Name: {item[1]} - Price: {item[2]}")    
    else:
        print("Item not found.")
def clear_memory():
    cur.execute("""DELETE FROM inventory""")
    cur.execute("DELETE FROM sqlite_sequence WHERE name = 'inventory'")
    con.commit()   
def update_item(upd_price,id):
    cur.execute("""UPDATE inventory SET price = ? WHERE id = ? 
    """,(upd_price,id))
    con.commit()
def delete_item(delete):
    cur.execute("""DELETE FROM inventory WHERE id = ? """,(delete,))
    con.commit()
    if cur.rowcount > 0:
        return "The item was delete , successfully"
    else :
        return "item not found"
    
while True :
    try:
        display_menu()
        choice = input("Enter your choice:").lower().strip()

        if choice == "a":
            name = input("Enter name of product: ").strip()
            price = float(input("Enter price of product: ").strip())
            result = add_item(name, price)
            if result:
                print(result)
            continue

        elif choice == "v":
            view_items()
            continue

        elif choice == "s":
            search_id = int(input("Enter ID of product to search:").strip())
            search_item(search_id)
            continue

        elif choice == "e":
            print("Exiting the program.")   
            break
        elif choice == "c":
            clear_memory()
            print("All items have been cleared from the inventory.")
        elif choice == "u":
            id = int(input("Enter id of the item you wish to Update: "))
            search_item(id)
            upd_price = float(input("Enter new price: "))
            update_item(upd_price,id)
            print("Item be update")
            search_item(id)
            print("-----------")
        elif choice == "d":
            delete = int(input("Enter id of the item you wish Delete: "))
            result = delete_item(delete)
            print(result)
        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

con.close()