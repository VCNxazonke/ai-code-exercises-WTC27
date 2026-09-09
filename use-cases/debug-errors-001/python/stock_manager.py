# stock_manager.py
"""
Stock Manager Inventory Reporting Module.
Fixed off-by-one index error using Pythonic enumerate iteration.
"""

def print_inventory_report(items):
    """
    Prints a formatted report of inventory items.
    
    Args:
        items (list[dict]): List of item dictionaries with 'name' and 'quantity' keys.
    """
    print("===== INVENTORY REPORT =====")
    # Fixed: Use Pythonic enumerate(items, start=1) to prevent IndexError
    for idx, item in enumerate(items, start=1):
        print(f"Item {idx}: {item['name']} - Quantity: {item['quantity']}")
    print("============================")

def main():
    items = [
        {"name": "Laptop", "quantity": 15},
        {"name": "Mouse", "quantity": 30},
        {"name": "Keyboard", "quantity": 25}
    ]
    print_inventory_report(items)

if __name__ == "__main__":
    main()
