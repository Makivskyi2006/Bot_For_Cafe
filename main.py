from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ------------------ CONFIG ------------------

# Put your BotFather token here:
TOKEN = "Your_Token"

# Your Telegram ID (orders will be sent to this chat)
ADMIN_CHAT_ID = Your_ID

# ------------------ DATA ------------------

# Simple restaurant menu. You can edit or expand it.
MENU = {
    "pizza_margherita": {"name": "Pizza Margherita", "price": 8.5},
    "pizza_pepperoni": {"name": "Pizza Pepperoni", "price": 9.9},
    "pasta_carbonara": {"name": "Pasta Carbonara", "price": 10.5},
    "salad_greek": {"name": "Greek Salad", "price": 6.0},
    "cola_05": {"name": "Coke 0.5L", "price": 2.5},
}

# user_id → {item_key: quantity}
CARTS = {}

# user_id → name
USER_NAMES = {}


# ------------------ HELPERS ------------------

def get_cart(user_id: int) -> dict:
    """Return user’s cart or create a new one."""
    if user_id not in CARTS:
        CARTS[user_id] = {}
    return CARTS[user_id]


def format_cart(cart: dict) -> str:
    """Create a readable message for the cart."""
    if not cart:
        return "🧺 Your cart is empty."

    lines = []
    total = 0.0

    for item_key, qty in cart.items():
        item = MENU.get(item_key)
        if item is None:
            continue

        price = item["price"]
        subtotal = qty * price
        total += subtotal
        lines.append(f"{item['name']} x{qty} — {subtotal:.2f}€")

    lines.append(f"\nTotal: {total:.2f}€")
    return "\n".join(lines)


# ------------------ COMMAND HANDLERS ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        f"Hi, {user.first_name}! 🍽\n\n"
        "Welcome to the restaurant bot.\n\n"
        "Commands:\n"
        "/menu – view menu\n"
        "/cart – view your cart\n"
        "/clear – clear your cart\n"
        "/checkout – place your order\n"
        "/name – set your name"
    )

    await update.message.reply_text(text)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []

    for key, item in MENU.items():
        label = f"{item['name']} — {item['price']:.2f}€"
        keyboard.append([
            InlineKeyboardButton(label, callback_data=f"add:{key}")
        ])

    await update.message.reply_text(
        "📋 Menu (tap an item to add it):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cart = get_cart(user_id)

    text = format_cart(cart)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Checkout", callback_data="checkout")]
    ])

    await update.message.reply_text(text, reply_markup=keyboard)


async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    CARTS[user_id] = {}
    await update.message.reply_text("🧹 Your cart has been cleared.")


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    cart = get_cart(user_id)
    if not cart:
        await update.message.reply_text("🧺 Your cart is empty.")
        return

    cart_text = format_cart(cart)
    user_name = USER_NAMES.get(user_id, "Unknown")

    # Confirmation for the user
    await update.message.reply_text("✅ Your order has been placed!\n\n" + cart_text)

    # Notification for admin
    if ADMIN_CHAT_ID:
        admin_msg = (
            f"📥 New order from @{user.username or user.first_name} (ID: {user_id})\n"
            f"Name: {user_name}\n\n"
            f"{cart_text}"
        )
        await context.bot.send_message(ADMIN_CHAT_ID, admin_msg)

    CARTS[user_id] = {}  # clear cart after checkout


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Commands:\n"
        "/menu – view menu\n"
        "/cart – view cart\n"
        "/clear – clear cart\n"
        "/checkout – checkout\n"
        "/name – set your name"
    )
    await update.message.reply_text(text)


# ------------------ NAME INPUT ------------------

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your name:")
    context.user_data["awaiting_name"] = True


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # If user is entering their name
    if context.user_data.get("awaiting_name"):
        USER_NAMES[user_id] = text
        context.user_data["awaiting_name"] = False
        await update.message.reply_text(f"Thanks! Your name was saved as: {text}")
        return

    # Other random messages
    await update.message.reply_text("I didn't understand. Try /menu, /cart, or /name.")


# ------------------ BUTTON CALLBACKS ------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user
    user_id = user.id

    # Add an item to cart
    if data.startswith("add:"):
        item_key = data.split(":", 1)[1]
        cart = get_cart(user_id)

        cart[item_key] = cart.get(item_key, 0) + 1

        item = MENU[item_key]
        await query.edit_message_text(
            f"{item['name']} was added to your cart! 🧺\n\n"
            "You can add more items from the menu.",
            reply_markup=query.message.reply_markup
        )

    # Checkout from button
    elif data == "checkout":
        cart = get_cart(user_id)

        if not cart:
            await query.edit_message_text("🧺 Your cart is empty.")
            return

        cart_text = format_cart(cart)
        user_name = USER_NAMES.get(user_id, "Unknown")

        await query.edit_message_text("✅ Your order has been placed!\n\n" + cart_text)

        if ADMIN_CHAT_ID:
            admin_msg = (
                f"📥 New order from @{user.username or user.first_name} (ID: {user_id})\n"
                f"Name: {user_name}\n\n"
                f"{cart_text}"
            )
            await context.bot.send_message(ADMIN_CHAT_ID, admin_msg)

        CARTS[user_id] = {}  # clear cart


# ------------------ MAIN ------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("cart", show_cart))
    app.add_handler(CommandHandler("clear", clear_cart))
    app.add_handler(CommandHandler("checkout", checkout))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("name", ask_name))

    # Button callbacks
    app.add_handler(CallbackQueryHandler(button_callback))

    # Text messages (used for name input)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
