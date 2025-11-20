🍽️ Restaurant Telegram Bot

A simple and clean Telegram bot built with Python and python-telegram-bot that allows users to:

view the restaurant menu

add items to their cart

enter their name

view and clear their cart

place an order

send orders directly to the admin

Perfect as a starting point for building a restaurant ordering system, food delivery bot, or internal kitchen bot.

🚀 Features
🧾 Menu System

Users can browse the menu and add food items with a single tap.

🧺 Shopping Cart

Each user gets their own cart:

add items

view cart

clear cart

checkout

👤 Name Input

Users can enter their name using /name, and this name will be included in the final order.

📩 Admin Notifications

Every completed order is automatically sent to the admin (your Telegram ID).

🔐 Per-User Storage

carts are stored per user

names are stored per user

📦 Requirements

Python 3.10+

python-telegram-bot v20+

Install dependencies:

pip install python-telegram-bot --upgrade

🛠️ Setup

Create a new bot using @BotFather

Copy your bot token

Find your Telegram user ID (via @getmyid_bot)

Open main.py and set:

TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_CHAT_ID = YOUR_USER_ID


Run the bot:

python main.py

💡 Available Commands
Command	Description
/start	Start the bot
/menu	Show the restaurant menu
/cart	Show your current cart
/clear	Clear your cart
/checkout	Place the order
/name	Enter your name
/help	List all commands
📬 Admin Order Notification

When a user places an order, the admin receives a message like:

📥 New order from @username (ID: 123456789)
Name: John

Pizza Margherita x2 — 17.00€
Coke 0.5L x1 — 2.50€

Total: 19.50€

🧱 Project Structure
RestaurantBot/
│
├── main.py        # main bot code
├── README.md      # project documentation
├── requirements.txt (optional)
└── .venv/         # virtual environment (optional)

🔧 Customization

You can easily expand this bot by adding:

phone number request

table number

delivery vs pickup

payment integration

JSON or SQLite order storage

admin panel with buttons

printable receipts

If you want help implementing any of these, just ask 😊

📝 License

This project is free to use, modify, and extend for personal or commercial purposes.

If you want, I can also make:

a GitHub-ready README with badges

a requirements.txt file

a logo/icon for your bot
