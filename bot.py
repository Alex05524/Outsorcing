import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dotenv import load_dotenv

from states import OrderForm, StatusForm
from keyboards import start_button_keyboard, main_menu_keyboard, edit_request_keyboard, services_keyboard, admin_panel_keyboard
from utils import save_order_to_json, get_order_status, update_order_status, load_orders, save_orders

# Загрузка переменных окружения
load_dotenv()

# Получение токена бота и ID админа
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
if not BOT_TOKEN or not ADMIN_ID:
    raise ValueError("Токен бота или ID админа не найден. Убедитесь, что переменные окружения BOT_TOKEN и ADMIN_ID заданы.")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Основная функция
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Обработка команды /start
    @dp.message(Command("start"))
    async def start_command(message: Message):
        await message.answer(
            "Добро пожаловать! Нажмите кнопку ниже, чтобы начать.",
            reply_markup=start_button_keyboard(),
        )

    # Обработка нажатия "Старт"
    @dp.callback_query(F.data == "start_work")
    async def start_work(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("Выберите действие из меню:", reply_markup=main_menu_keyboard())

    # Обработка кнопки "Услуги"
    @dp.callback_query(F.data == "services")
    async def show_services(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("Выберите услугу:", reply_markup=services_keyboard())

    # Обработка кнопки "Компьютерная помощь"
    @dp.callback_query(F.data == "service_1")
    async def computer_help(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text(
            "Мы предлагаем:\n"
            "— Полный аутсорсинг для ИП, ТОО и любых других форм бизнеса.\n"
            "— Установка любых программ, необходимых для работы.\n"
            "— Удалённая настройка через TeamViewer, AnyDesk, Ammyy Admin — быстро и удобно.\n\n"
            "Комплексные услуги для вашей техники:\n"
            "— Установка Windows (10, 11, Server) и Office (2007–2021+).\n"
            "— Настройка драйверов для стабильной работы.\n"
            "— Профессиональная чистка ноутбуков и ПК.\n"
            "— Оптимизация систем для максимальной производительности.",
            reply_markup=services_keyboard()
        )

    # Обработка кнопки "Предложения по монтажным работам"
    @dp.callback_query(F.data == "service_2")
    async def installation_proposals(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text(
            "Устали от медленного интернета, обрывов соединения и хаоса с проводами?\n"
            "Мы предлагаем профессиональный монтаж локальных сетей \"под ключ\" для вашего дома, офиса или предприятия!\n\n"
            "Почему выбирают нас?\n"
            "Высокая скорость и стабильность: Мы проектируем и настраиваем сети, которые работают без перебоев.\n"
            "Индивидуальный подход: Решения, идеально подходящие под ваши задачи и бюджет.\n"
            "Современные технологии: Используем только проверенные материалы и оборудование.\n"
            "Квалифицированные специалисты: У нас работают опытные инженеры с более чем 5-летним опытом.\n"
            "Гарантия качества: Даем гарантию на все выполненные работы и материалы.\n\n"
            "Мы предлагаем:\n"
            "Проектирование сети: Разработка схем подключения с учётом ваших потребностей.\n"
            "Монтаж и настройка: Установка кабельной системы, Wi-Fi точек, маршрутизаторов и другого оборудования.\n"
            "Техническая поддержка: Обслуживание сетей и оперативное решение любых вопросов.",
            reply_markup=services_keyboard()
        )

    # Обработка кнопки "Заказ на выезд"
    @dp.callback_query(F.data == "service_3")
    async def order_visit(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text("Пожалуйста, введите ваше полное имя для оформления заявки:")
        await state.set_state(OrderForm.full_name)

    # Обработка кнопки "Оформить заявку"
    @dp.callback_query(F.data == "apply_request")
    async def create_request(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text("Пожалуйста, введите ваше полное имя:")
        await state.set_state(OrderForm.full_name)

    # Обработка кнопки "Статус заявки"
    @dp.callback_query(F.data == "status_request")
    async def check_status(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text("Пожалуйста, введите номер вашей заявки (ID):")
        await state.set_state(StatusForm.request_id)

    # Обработчик получения статуса заявки
    @dp.message(StatusForm.request_id)
    async def handle_status_request(message: Message, state: FSMContext):
        try:
            order_id = int(message.text)
            status = get_order_status(order_id)
        except ValueError:
            status = "Неверный формат ID. Пожалуйста, введите число ID."
        await message.answer(status)
        await state.clear()

    # Обработка ввода полного имени для новой заявки
    @dp.message(OrderForm.full_name)
    async def process_full_name(message: Message, state: FSMContext):
        full_name = message.text
        await state.update_data(full_name=full_name)
        await message.answer("Введите ваш адрес:")
        await state.set_state(OrderForm.address)

    # Обработка ввода адреса
    @dp.message(OrderForm.address)
    async def process_address(message: Message, state: FSMContext):
        address = message.text
        await state.update_data(address=address)
        await message.answer("Введите ваш номер телефона:")
        await state.set_state(OrderForm.phone_number)

    # Обработка ввода номера телефона
    @dp.message(OrderForm.phone_number)
    async def process_phone_number(message: Message, state: FSMContext):
        phone_number = message.text
        await state.update_data(phone_number=phone_number)
        await message.answer("Введите причину обращения:")
        await state.set_state(OrderForm.reason)

    # Обработка ввода причины обращения
    @dp.message(OrderForm.reason)
    async def process_reason(message: Message, state: FSMContext):
        reason = message.text
        await state.update_data(reason=reason)
        order_data = await state.get_data()
        order_id = save_order_to_json(order_data)
        
        await message.answer(
            f"Заявка #{order_id} успешно оформлена!\n"
            f"Имя: {order_data['full_name']}\n"
            f"Адрес: {order_data['address']}\n"
            f"Телефон: {order_data['phone_number']}\n"
            f"Причина обращения: {order_data['reason']}"
        )

        await state.clear()

    @dp.callback_query(F.data == "edit_request")
    async def edit_request(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text(
            "Выберите, что вы хотите изменить:",
            reply_markup=edit_request_keyboard()
        )
    
    @dp.callback_query(F.data == "edit_name")
    async def edit_name(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text("Введите новое имя:")
        await state.set_state(OrderForm.full_name)

    @dp.callback_query(F.data == "edit_address")
    async def edit_address(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text("Введите новый адрес:")
        await state.set_state(OrderForm.address)
    
    @dp.callback_query(F.data == "edit_phone")
    async def edit_phone(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.edit_text("Введите новый номер телефона:")
        await state.set_state(OrderForm.phone_number)

    # Обработка кнопки "Назад" в меню услуг
    @dp.callback_query(F.data == "back_to_main")
    async def back_to_main(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("Выберите действие из меню:", reply_markup=main_menu_keyboard())

    # Обработка кнопки "Панель администратора"
    @dp.callback_query(F.data == "admin_panel")
    async def admin_panel(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("Панель администратора:", reply_markup=admin_panel_keyboard())

    # Обработка кнопки "Обработано"
    @dp.callback_query(F.data == "processed_1")
    async def process_order(callback_query: CallbackQuery):
        try:
            order_id = int(callback_query.data.split('_')[1])
            await update_order_status_and_notify(callback_query, order_id, 'Обработано')
        except (IndexError, ValueError):
            await callback_query.answer("Ошибка при извлечении ID заявки. Повторите попытку.")

    # Обработка кнопки "В работе" 
    @dp.callback_query(F.data == "in_progress_1")
    async def in_progress_order(callback_query: CallbackQuery):
        try:
            order_id = int(callback_query.data.split('_')[1])
            await update_order_status_and_notify(callback_query, order_id, 'В работе')
        except (IndexError, ValueError):
            await callback_query.answer("Ошибка при извлечении ID заявки. Повторите попытку.")

    async def update_order_status_and_notify(callback_query: CallbackQuery, order_id: int, new_status: str):
        """Обновление статуса заявки и уведомление о результате."""
        success = update_order_status(order_id, new_status)
        
        if success:
            await callback_query.answer(f"Заявка {order_id} теперь имеет статус: {new_status}")
        else:
            await callback_query.answer(f"Не удалось обновить статус заявки с ID {order_id}. Попробуйте позже.")  

    @dp.update()
    async def handle_update(update: types.Update):
        try:
            if isinstance(update, types.Message):
                logging.info(f"Обновление с ID={update.update_id} обработано успешно.")
            elif isinstance(update, types.CallbackQuery):
                logging.info(f"Обновление с ID={update.update_id} обработано как callback.")
            else:
                logging.info(f"Обновление с ID={update.update_id} обработано другого типа.")
        except Exception as e:
             logging.error(f"Ошибка при обработке обновления с ID={update.update_id}: {e}")

    @dp.errors()
    async def handle_error(update: types.Update, exception: Exception):
        logging.error(f"Необработанное обновление с ID={update.update_id}. Ошибка: {exception}")

    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Бот остановлен.")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
