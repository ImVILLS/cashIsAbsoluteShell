import os

# Определяем путь к папке Cash (где находится cash.py)
CASH_DIR = os.path.dirname(os.path.abspath(__file__))
# Теперь файл в папке Cash
HISTORY_FILE = os.path.join(CASH_DIR, "history.log")


def log_command(command):
    """Сохраняет команду в history.log"""
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(command + "\n")


def show_history():
    """Выводит историю команд"""
    if not os.path.exists(HISTORY_FILE):
        print("История команд пуста.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        print(f"{i}. {line.strip()}")


def clear_history():
    """Очищает историю команд"""
    open(HISTORY_FILE, "w").close()
    print("История команд очищена.")
