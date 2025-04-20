from prompt_toolkit import prompt
from commands import exec_command, update_autocomplete
from config import get_config
from rich import print
import os
import socket
from prompt_toolkit.formatted_text import HTML
from users import users, current_user
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.application import get_app


def show_welcome():
    """Выводит кастомное приветствие"""
    message = get_config("appearance", "welcome_message",
                         "Добро пожаловать в Cash!")
    color = get_config("appearance", "welcome_color", "cyan")
    print(f"[{color}]{message}[/{color}]")


def update_prompt():
    """Обновляет строку промпта после смены пользователя"""
    user = current_user()
    host = socket.gethostname()
    path = os.getcwd()

    prompt_format = get_config(
        "appearance", "prompt_format", "[{user}@{host}]$ {path}")
    prompt_style = get_config("appearance", "prompt_style", "green")

    prompt = prompt_format.replace("{user}", user).replace(
        "{host}", host).replace("{path}", path)

    # Очищаем экран и заставляем `prompt_toolkit` обновить вывод
    clear()
    get_app().output.flush()

    print(f"[{prompt_style}]{prompt}[/{prompt_style}]", end="")


def get_prompt():
    """Создаёт кастомный промпт с актуальным пользователем"""
    user = users["current"]
    host = socket.gethostname()
    path = os.getcwd()

    prompt_format = get_config(
        "appearance", "prompt_format", "[{user}@{host}]$ {path}")
    prompt_style = get_config("appearance", "prompt_style", "green")

    prompt = prompt_format.replace("{user}", user).replace(
        "{host}", host).replace("{path}", path)

    return HTML(f'<{prompt_style}>{prompt}</{prompt_style}> ')


def main():
    """Главный цикл Cash с обработкой ошибок"""
    print(f"\n{get_config('appearance', 'MOTD',
          'Сегодня отличный день!')}\n")  # Выводим MOTD

    while True:
        try:
            command = prompt(
                get_prompt(), completer=update_autocomplete()).strip()
            if command:
                exec_command(command)
        except KeyboardInterrupt:
            print("\nВыход из Cash.")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
