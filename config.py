# config.py
import os
import configparser

CONFIG_PATH = os.path.expanduser("~/.config/cash/cash.conf")

# Устанавливаем значения по умолчанию
default_config = {
    "appearance": {
        "prompt_format": "[{user}@{host}]$ {path}",
        "MOTD": "Добро пожаловать в Cash!",
        "welcome_color": "cyan",
        "prompt_style": "green"
    }
}

config = configparser.ConfigParser()


def convert_old_config():
    """Автоматически обновляет старый формат `cash.conf` в INI"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if lines and "=" in lines[0]:  # Проверяем, есть ли старый формат
            print("[DEBUG] Обнаружен старый формат cash.conf. Автообновление...")
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write("[appearance]\n")
                for line in lines:
                    key, value = line.strip().split("=", 1)
                    key = key.lower().replace("prompt", "prompt_style")  # Исправляем ключи
                    f.write(f"{key.strip()} = {value.strip().strip('\"')}\n")
            print("[DEBUG] Конфигурация обновлена!")
    except Exception as e:
        print(f"[ERROR] Ошибка при обновлении cash.conf: {e}")


def load_config():
    """Загружает конфигурацию, создаёт файл, если его нет"""
    if not os.path.exists(CONFIG_PATH):
        save_config()

    config.read(CONFIG_PATH)


def save_config():
    """Сохраняет текущие настройки в файл"""
    with open(CONFIG_PATH, "w") as f:
        config.write(f)


def get_config(section, option, default=None):
    """Получает значение из конфигурации"""
    return config.get(section, option, fallback=default)


def set_config(section, option, value):
    """Устанавливает значение и сохраняет"""
    if section not in config:
        config[section] = {}
    config[section][option] = value
    save_config()


# Загружаем конфигурацию при старте
load_config()
