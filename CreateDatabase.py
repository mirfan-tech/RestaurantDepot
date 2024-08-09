import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('items.db')
c = conn.cursor()

# Create a table
c.execute('''
CREATE TABLE items (
    ItemNo INTEGER PRIMARY KEY AUTOINCREMENT,
    Items TEXT,
    Category TEXT,
    AisleNo TEXT,
    Store TEXT
)
''')

# Sample data - you'll need to insert all your data here
data = [
    ("Onion-red","Vegetables","NA","Restaurant Depot"),
    ("Onion-white","Vegetables","NA","Restaurant Depot"),
    ("Cilantro","Vegetables","NA","Restaurant Depot"),
    ("Mint Leaf","Vegetables","NA","Restaurant Depot"),
    ("Bell Pepper","Vegetables","NA","Restaurant Depot"),
    ("Spring Onion (Green Onion)","Vegetables","NA","Restaurant Depot"),
    ("Beet Root","Vegetables","NA","Restaurant Depot"),
    ("Red Cabbage","Vegetables","NA","Restaurant Depot"),
    ("Green Beans","Vegetables","NA","Restaurant Depot"),
    ("Garlic","Vegetables","NA","Restaurant Depot"),
    ("Salt - 50 lbs","Pantry","A0205","Restaurant Depot"),
    ("Sugar Granulated - 50 lbs","Pantry","A0207","Restaurant Depot"),
    ("SoyaBean Oil","Pantry","A1401","Restaurant Depot"),
    ("Fry Oil","Pantry","A1404","Restaurant Depot"),
    ("Seseame Oil","Pantry","NA","Restaurant Depot"),
    ("Pan Release Spray","Pantry","A1404","Restaurant Depot"),
    ("Lemon Yellow Food Colour","Pantry","NA","Restaurant Depot"),
    ("Soy Sauce","Pantry","NA","Restaurant Depot"),
    ("Ketchup","Pantry","NA","Restaurant Depot"),
    ("Fruit Punch Drink Base","Pantry","A0218","Restaurant Depot"),
    ("Lemonade Drink Base","Pantry","A0218","Restaurant Depot"),
    ("Corn Starch","Pantry","A0306","Restaurant Depot"),
    ("Dry Chilli","Pantry","A0611","Restaurant Depot"),
    ("Tomato Puree - Isabella","Pantry","A0707","Restaurant Depot"),
    ("Kyrol","Pantry","A0307","Restaurant Depot"),
    ("All Purpose Flour","Pantry","A0310","Restaurant Depot"),
    ("Royal Basmati Rice","Pantry","A0400","Restaurant Depot"),
    ("White Rice (Extra Large Grain)","Pantry","A0400","Restaurant Depot"),
    ("Garbanzo [Channa]","Pantry","A0413","Restaurant Depot"),
    ("Chocolate Syrup","Pantry","NA","Restaurant Depot"),
    ("Caramel Syrup","Pantry","NA","Restaurant Depot"),
    ("Chocolate Chips","Pantry","A0210","Restaurant Depot"),
    ("Chocolate Bar","Pantry","A0210","Restaurant Depot"),
    ("Liquid Margarine","Dairy","NA","Restaurant Depot"),
    ("Puff Sheet","Pantry","NA","Restaurant Depot"),
    ("Vegitable Shortening","Pantry","NA","Restaurant Depot"),
    ("Coffee Beans","Pantry","A0314","Restaurant Depot"),
    ("Raw Sugar","Pantry","A0517","Restaurant Depot"),
    ("Pure Cane Sugar","Pantry","A0517","Restaurant Depot"),
    ("Splenda","Pantry","A0517","Restaurant Depot"),
    ("Paneer","Dairy","NA","Restaurant Depot"),
    ("Cheese","Dairy","NA","Restaurant Depot"),
    ("Wax paper","Bakery","NA","Restaurant Depot"),
    ("Milk Cream","Dairy","A3037","Restaurant Depot"),
    ("Milk","Dairy","A3039","Restaurant Depot"),
    ("Yogurt","Dairy","A3055","Restaurant Depot"),
    ("Butter","Dairy","A3058","Restaurant Depot"),
    ("Stainless Steel Scrub","Cleaning Supplies","NA","Restaurant Depot"),
    ("Surface Liquid","Cleaning Supplies","NA","Restaurant Depot"),
    ("HILITE Dishwashing soap","Cleaning Supplies","A0801","Restaurant Depot"),
    ("Clorox","Cleaning Supplies","A0805","Restaurant Depot"),
    ("Fabuloso","Cleaning Supplies","A0807","Restaurant Depot"),
    ("Trash Cover (Small)","Cleaning Supplies","A0816","Restaurant Depot"),
    ("Trash cover (Big)","Cleaning Supplies","A08161","Restaurant Depot"),
    ("Bounty","Cleaning Supplies","A0907","Restaurant Depot"),
    ("Water Bottle","Beverage","A1222","Restaurant Depot"),
    ("Candy","Candy","A1601","Restaurant Depot"),
    ("Medium Bag","Packaging","NA","Restaurant Depot"),
    ("Big Bag","Packaging","NA","Restaurant Depot"),
    ("Small Bag","Packaging","NA","Restaurant Depot"),
    ("3.25 oz container","Packaging","A1109","Restaurant Depot"),
    ("3.25 oz & 4 oz Lids","Packaging","A1109","Restaurant Depot"),
    ("4 oz container","Packaging","A1110","Restaurant Depot"),
    ("16 oz Round Box","Packaging","NA","Restaurant Depot"),
    ("28 oz Squre Box","Packaging","NA","Restaurant Depot"),
    ("2 oz Cups","Packaging","NA","Restaurant Depot"),
    ("2 oz Lids","Packaging","NA","Restaurant Depot"),
    ("water Cups","Packaging","NA","Restaurant Depot"),
    ("9 x 9 Dosa Box","Packaging","NA","Restaurant Depot"),
    ("9 x 6 Idli Vada Box","Packaging","NA","Restaurant Depot"),
    ("6 x 6 Idli Box","Packaging","A1009","Restaurant Depot"),
    ("24 oz Square Box","Packaging","A1012","Restaurant Depot"),
    ("Foil (18 x 1000)","Packaging","NA","Restaurant Depot"),
    ("Plastic Knife","Packaging","NA","Restaurant Depot"),
    ("Plastic Spoon","Packaging","A0902","Restaurant Depot"),
    ("Plastic Fork","Packaging","A0903","Restaurant Depot"),
    ("Mango Lassi Cup (9 oz)","Packaging","NA","Restaurant Depot"),
    ("Lassi Cup lids","Packaging","NA","Restaurant Depot"),
    ("Coffee cup Lids","Packaging","NA","Restaurant Depot"),
    ("Mango Lassi Cup (12 oz)","Packaging","A1302","Restaurant Depot"),
    ("Coffee Cups (8 oz)","Packaging","A1307","Restaurant Depot"),
    ("Coffee Stirrer","Packaging","A1309","Restaurant Depot"),
    ("Straw 7.75 Wrapped Giant red","Packaging","A1313","Restaurant Depot"),
    ("Gloves (Medium, Large Size)","Packaging","NA","Restaurant Depot"),
    ("Dinner Napkins","Packaging","A0915","Restaurant Depot"),
    ("Sanitizer","Personal Hygiene","NA","Restaurant Depot"),
    ("4 inch Half Trays","Packaging","NA","Restaurant Depot"),
    ("2 inch Full Trays","Packaging","NA","Restaurant Depot"),
    ("2 inch Half Trays","Packaging","NA","Restaurant Depot"),
    ("half Tray Lids","Packaging","NA","Restaurant Depot"),
    ("Paper Plate Round - Plain","Packaging","A0907","Restaurant Depot"),
    ("Paper Plate Round - Compartment","Packaging","A0908","Restaurant Depot"),
    ("Chafing fuel","Packaging","A1204","Restaurant Depot"),
    ("4 inch Full Trays","Packaging","A1206","Restaurant Depot"),
    ("Fulll Tray Lids","Packaging","A1206","Restaurant Depot")

    # Add all other items similarly...
]

# Insert data into the table
c.executemany('INSERT INTO items (Items, Category, AisleNo, Store) VALUES (?, ?, ?, ?)', data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and data inserted successfully!")
