from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def start_button_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🚀 Старт", callback_data="start_work")]]
    )

def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[  
        [InlineKeyboardButton(text="📋 Услуги", callback_data="services")],
        [InlineKeyboardButton(text="📝 Оформить заявку", callback_data="apply_request")],
        [InlineKeyboardButton(text="📦 Статус заявки", callback_data="status_request")],
        [InlineKeyboardButton(text="✏️ Редактировать заявку", callback_data="edit_request")],
        [InlineKeyboardButton(text="🔧 Панель администратора", callback_data="admin_panel")],
    ])

def services_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Компьютерная помощь", callback_data="service_1")],
        [InlineKeyboardButton(text="Предложения по монтажным работам", callback_data="service_2")],
        [InlineKeyboardButton(text="Заказ на выезд", callback_data="service_3")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ])

def edit_request_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать имя", callback_data="edit_name")],
        [InlineKeyboardButton(text="Редактировать адрес", callback_data="edit_address")],
        [InlineKeyboardButton(text="Редактировать телефон", callback_data="edit_phone")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ])

def admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обработано", callback_data="processed_1")],
        [InlineKeyboardButton(text="В работе", callback_data="in_progress_1")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ])