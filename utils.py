import json
import os
import logging

# Указываем абсолютный путь к файлу orders.json
ORDERS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'orders.json')

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Используемый путь к файлу: {ORDERS_FILE_PATH}")

def load_orders():
    try:
        with open('orders.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Файл orders.json не найден")
        return []
    except json.JSONDecodeError:
        logging.error("Ошибка декодирования JSON файла")
        return [
            {"full_name": "123", "address": "123", "phone_number": "123", "reason": "123", "id": 1, "status": "Ожидает обработки"}
        ]

def save_orders(orders):
    with open('orders.json', 'w', encoding='utf-8') as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)
        pass

def save_order_to_json(order_data: dict) -> int:
    """Сохраняет заявку на выезд в JSON и возвращает её ID."""
    data = load_orders()
    if not isinstance(data, list):
        logging.error("Не удалось загрузить заявки: данные не в правильном формате.")
        return -1

    next_id = max([order.get("id", 0) for order in data], default=0) + 1
    order_data["id"] = next_id
    order_data["status"] = "Ожидает обработки"  # Устанавливаем статус по умолчанию
    data.append(order_data)
    save_orders(data)
    logging.info(f"Заявка #{next_id} успешно сохранена.")
    return next_id

def get_order_status(order_id: int) -> str:
    """Возвращает статус заявки по её ID."""
    orders = load_orders()
    if not isinstance(orders, list):
        return "Ошибка загрузки заявок"

    for order in orders:
        if order["id"] == order_id:
            reason = order.get("reason", "Причина не указана")
            status = order.get("status", "Статус не указан")
            return f"{reason}\n{status}"

    logging.info(f"Заявка #{order_id} не найдена.")
    return "Заявка не найдена"

def on_button_click():
    logging.info("Кнопка нажата, начинаем запрос ID заявки.")
    order_id = input("Введите ID заказа для обновления статуса: ")
    if order_id:
        order_id = int(order_id)
        new_status = "Обработано"
        logging.info(f"Получен ID заказа: {order_id}. Пытаемся обновить статус.")
        update_order_status(order_id, new_status)
    else:
        logging.error("Не был введен ID заказа.")

# Функция для поиска и изменения статуса заявки по ID
def update_order_status(order_id, new_status):
    try:
        # Чтение данных из файла orders.json
        with open("orders.json", "r", encoding="utf-8") as file:
            orders = json.load(file)

        logging.info(f"Чтение данных из файла успешно. Содержимое: {orders}")

        # Ищем заказ по ID
        order = next((order for order in orders if order["id"] == order_id), None)

        if order:
            current_status = order["status"]
            logging.info(f"Текущий статус заказа с ID {order_id}: {current_status}")

            # Условие, при котором статус изменяется
            if current_status in ["Ожидает обработки", "В работе"]:
                order["status"] = new_status
                logging.info(f"Статус заказа с ID {order_id} изменён с '{current_status}' на '{new_status}'")

                # Сохраняем изменения обратно в файл
                with open("orders.json", "w", encoding="utf-8") as file:
                    json.dump(orders, file, indent=4, ensure_ascii=False)

                logging.info("Файл orders.json успешно обновлен.")
                return True
            else:
                logging.info(f"Статус заказа с ID {order_id} не требует изменений, так как он уже: {current_status}")
                return False

        else:
            logging.warning(f"Заявка с ID {order_id} не найдена.")
            return False

    except FileNotFoundError:
        logging.error("Файл orders.json не найден.")
    except json.JSONDecodeError:
        logging.error("Ошибка при чтении JSON файла.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    return False