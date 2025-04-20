import os
import json
import sys
import importlib
from prompt_toolkit.shortcuts import clear

USERS_FILE = "users.json"

# Загружаем пользователей из файла

CURRENT_USER = "sa"  # Глобальная переменная пользователя


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": ["sa"], "current": "sa"}  # sa = System Admin (root)

# Сохраняем пользователей в файл


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


users = load_users()


def add_user(username):
    """Добавляет пользователя с проверкой аргументов"""
    try:
        if not username:
            print("Ошибка: укажите имя пользователя.")
            return
        if username in users["users"]:
            print(f"Ошибка: пользователь {username} уже существует.")
        else:
            users["users"].append(username)
            save_users(users)
            print(f"Пользователь {username} добавлен.")
    except Exception as e:
        print(f"❌ Ошибка при добавлении пользователя: {e}")


def remove_user(username):
    """Удаляет пользователя"""
    if username == "sa":
        print("Ошибка: нельзя удалить sa.")
    elif username not in users["users"]:
        print(f"Ошибка: пользователь {username} не найден.")
    else:
        users["users"].remove(username)
        save_users(users)
        print(f"Пользователь {username} удалён.")


def current_user():
    """Выводит текущего пользователя"""
    users = load_users()  # Загружаем свежие данные
    return users["current"]


def su(params):
    """Меняет пользователя и перезапускает Cash"""
    if not params:
        print("Ошибка: используйте su <имя_пользователя>")
        return

    new_user = "".join(params).strip()
    if not new_user:
        print("Ошибка: пустое имя пользователя")
        return

    users = load_users()
    if new_user not in users["users"]:
        print(f"Ошибка: пользователь {new_user} не найден.")
        return

    # Обновляем текущего пользователя
    users["current"] = new_user
    save_users(users)

    # Очищаем экран
    clear()

    print(f"Теперь вы {new_user}.")

    # Полностью перезапускаем Cash, чтобы обновился prompt
    os.execv(sys.executable, [sys.executable] + sys.argv)


def chown(file, username):
    """Меняет владельца файла"""
    if username not in users["users"]:
        print(f"Ошибка: пользователь {username} не найден.")
    elif not os.path.exists(file):
        print(f"Ошибка: файл {file} не найден.")
    else:
        os.chown(file, os.getuid(), os.getgid())  # Работает только в Unix
        print(f"Файл {file} теперь принадлежит {username}.")


def permod(file, mode):
    """Изменяет права доступа к файлу"""
    if not os.path.exists(file):
        print(f"Ошибка: файл {file} не найден.")
    else:
        os.chmod(file, int(mode, 8))  # Пример: "755" → 0o755
        print(f"Права файла {file} изменены на {mode}.")
