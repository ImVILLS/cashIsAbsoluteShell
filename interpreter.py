from history import log_command
from custom import commands_dict, define_coma, remove_coma  # Теперь корректно


def exec_script(script_name, script_args):
    """Запускает .cas-скрипт и логирует команды"""
    try:
        with open(script_name, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            command = line.strip()
            if not command or command.startswith("//"):
                continue  # Игнорируем пустые строки и комментарии

            # Подставляем аргументы
            for i, arg in enumerate(script_args):
                command = command.replace(f"*arg{i+1}*", arg)

            print(f"[DEBUG] Выполняем команду из скрипта: {command}")

            from commands import exec_command
            exec_command(command)

    except FileNotFoundError:
        print(f"Ошибка: файл '{script_name}' не найден.")
    except Exception as e:
        print(f"Ошибка при выполнении {script_name}: {e}")
