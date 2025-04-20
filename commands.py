import os
import shutil
import sys
import subprocess
import platform
from history import show_history, clear_history
from users import add_user, remove_user, current_user, su, chown, permod
from rich.console import Console
from rich.table import Table
from prompt_toolkit.completion import WordCompleter
from interpreter import exec_script
from custom import commands_dict, define_coma, remove_coma, variables

console = Console()


# Базовые команды
command_list = [
    "list", "goto", "mo", "co", "rm", "make", "fear", "find",
    "sysfetch", "clr", "history", "addu", "remu", "curru", "su",
    "chown", "permod", "run", "exit", "owl", "help", "oput",
    "coma", "codel"
]

# Создаём объект для автодополнения
completer = WordCompleter(command_list, ignore_case=True)


def update_autocomplete(new_command=None):
    """Обновляет список автодополнения при добавлении новых команд"""
    global completer
    if new_command and new_command not in command_list:
        command_list.append(new_command)  # Добавляем новую команду
    return WordCompleter(command_list, ignore_case=True)


def list():
    print("List of files in the current directory:")
    for file in os.listdir():
        print(file)


def goto(path):
    try:
        os.chdir(path)
        print(f"Перешли в {os.getcwd()}")
    except FileNotFoundError:
        print("Directory not found")
    except IndexError:
        print("No directory specified")
    except PermissionError:
        print("Permission denied")


def mo(params):  # mo - move object. Object - file or directory
    try:
        shutil.move(params[-1], params[1])
        print(f"{params[-1]} перемещён в {params[1]}")
    except FileNotFoundError:
        print("File not found")
    except IndexError:
        print("No file specified")
    except PermissionError:
        print("Permission denied")


def co(params):
    if len(params) < 1:
        print("Ошибка: укажите источник и цель")
        return
    try:
        shutil.copy(params[-1], params[1])
        print(f"{params[-1]} скопирован в {params[1]}")
    except FileNotFoundError:
        print(f"Ошибка: {params[-1]} не найден")
    except PermissionError:
        print(f"Ошибка: нет прав на копирование {params[-1]}")
    except Exception as e:
        print(f"Ошибка: {e}")


def rm(params):
    if not params:
        print("Ошибка: укажите файл или папку")
        return
    target = params[-1]
    try:
        if os.path.isdir(target):
            os.rmdir(target)
            print(f"Удалена директория: {target}")
        elif os.path.isfile(target):
            os.remove(target)
            print(f"Удалён файл: {target}")
        else:
            print(f"Ошибка: {target} не найден")
    except PermissionError:
        print(f"Ошибка: нет прав на удаление {target}")
    except Exception as e:
        print(f"Ошибка: {e}")


def make(params):
    if len(params) < 1:
        print("Ошибка: укажите -d (директория) или -f (файл) и имя")
        return
    option, name = params
    try:
        if option == "-d":
            os.makedirs(name, exist_ok=True)
            print(f"Создана директория: {name}")
        elif option == "-f":
            open(name, "w").close()
            print(f"Создан файл: {name}")
        else:
            print("Ошибка: неизвестный флаг. Используйте -d или -f")
    except PermissionError:
        print(f"Ошибка: нет прав на создание {name}")
    except Exception as e:
        print(f"Ошибка: {e}")


def fear(params):
    """Открывает файл в редакторе Fear"""
    if len(params) < 1:
        print("Ошибка: укажите файл. Использование: fear <файл> [-r|-e]")
        return

    fear_script = os.path.join(os.path.dirname(__file__), "fear.py")

    if not os.path.exists(fear_script):
        print("Ошибка: файл `fear.py` не найден.")
        return

    try:
        subprocess.run(["python", fear_script] + params, check=True)
    except Exception as e:
        print(f"Ошибка при запуске Fear: {e}")


def find(params):
    if not params:
        print("Ошибка: укажите имя файла или папки")
        return
    target = params[-1]
    detailed = "-i" in params

    if os.path.exists(target):
        print(f"{target} найден")
        if detailed:
            size = os.path.getsize(target)
            print(f"Размер: {size} байт")
            print("Тип:", "Файл" if os.path.isfile(target) else "Директория")
    else:
        print(f"{target} не найден")


def run(params):
    """Выполняет .cas-скрипт"""
    if len(params) < 1:
        print("Ошибка: укажите файл. Использование: run <файл.cas>")
        return

    script_file = params[0]

    if not os.path.exists(script_file):
        print(f"Ошибка: файл '{script_file}' не найден.")
        return

    try:
        exec_script(script_file, params[1:])  # Передаём аргументы в скрипт
    except Exception as e:
        print(f"Ошибка при выполнении {script_file}: {e}")


def sysfetch():
    print("System information:")
    print("OS:", platform.system())
    print("Version:", platform.version())
    print("Release:", platform.release())
    print("Architecture:", platform.architecture())
    print("Machine:", platform.machine())
    print("Processor:", platform.processor())
    print("Shell: cash 0.3.1")


def clr():
    os.system("cls" if os.name == "nt" else "clear")


def help():
    """Выводит список доступных команд в виде красивой таблицы"""
    table = Table(title="Cash Commands", header_style="bold cyan")

    table.add_column("Команда", style="bold white")
    table.add_column("Описание", style="bold yellow")

    commands = {
        "list": "Показать файлы в текущей директории",
        "goto <путь>": "Перейти в указанную директорию",
        "mo <старое> <новое>": "Переместить файл или директорию",
        "co <файл1> <файл2>": "Копировать файл",
        "rm <файл> [-r]": "Удалить файл или директорию",
        "make <-d|-f> <имя>": "Создать директорию или файл",
        "fear <файл> [-r|-e]": "Открыть файл в редакторе",
        "find <файл> [-i]": "Найти файл, -i для информации",
        "sysfetch": "Вывести информацию о системе",
        "clr": "Очистить терминал",
        "history": "Показать историю команд",
        "clr -h": "Очистить историю команд",
        "addu <имя>": "Добавить пользователя",
        "remu <имя>": "Удалить пользователя",
        "curru": "Показать текущего пользователя",
        "su <имя>": "Сменить пользователя",
        "chown <файл> <пользователь>": "Изменить владельца файла",
        "permod <файл> <права>": "Изменить права файла",
        "codel": "Удалить пользовательские команды",
        "run <файл.cas>": "Запустить Cash-скрипт",
        "exit": "Выйти из Cash",
        "owl": "Вывести ASCII-сову"
    }

    for cmd, desc in commands.items():
        table.add_row(cmd, desc)

    console.print(table)


def coma(params):
    """Создаёт кастомную команду с `&` для объединения"""
    if len(params) < 2:
        print("Ошибка: используйте coma <имя> <команда> & <команда> ...")
        return

    name = params[0]
    command_body = " ".join(params[1:]).replace("\\", "").strip()

    # Разбиваем команды по `&` и сохраняем как СПИСОК
    commands = [cmd.strip() for cmd in command_body.split("&")]

    define_coma(name, commands)  # Сохраняем список, а не строку
    print(f"Добавлена кастомная команда: {name}")


def codel(params):
    """Удаляет кастомную команду"""
    if params:
        name = params[0]
        if name in commands_dict:
            remove_coma(name)  # Используем `remove_coma()` из `custom.py`
            print(f"Кастомная команда `{name}` удалена.")
        else:
            print(f"Ошибка: команды `{name}` не существует.")
    else:
        commands_dict.clear()
        print("Все кастомные команды удалены.")


def exit():
    print("Exiting")
    sys.exit(-1)


def owl():  # prints owl ascii art and the message "Hoo-hoo!"
    print("  ___")
    print(" (o,o)")
    print(" /)__)")
    print("  Hoo-hoo!")


def oput(params):
    """Выводит текст в консоль"""
    if not params:
        print("Ошибка: oput требует аргумент. Использование: oput <текст>")
        return

    text = " ".join(params)

    # Подставляем переменные (*var*)
    for var, value in variables.items():
        text = text.replace(f"*{var}*", value)

    print(text)


def exec_command(command):
    """Обрабатывает команды, включая кастомные"""
    from history import log_command

    parts = command.split()
    if not parts:
        return

    parts = command.split()
    cmd = parts[0]
    params = parts[1:]

    # Проверяем, есть ли команда в кастомных
    if cmd in commands_dict:
        print(f"[DEBUG] Выполняем кастомную команду `{cmd}`")

        # Выполняем каждую команду из списка `coma`
        for sub_command in commands_dict[cmd]:
            log_command(sub_command)  # Логируем выполнение
            exec_command(sub_command)  # Выполняем команду
        return

    log_command(command)

    match cmd:
        case "oput":
            oput(params)
        case "run":
            run(params)
        case "coma":
            coma(params)
        case "codel":
            codel(params)
        case "history":
            show_history()
        case "clr" if "-h" in command:
            clear_history()
        case "addu":
            add_user(params[0])
        case "remu":
            remove_user(params[0])
        case "curru":
            print(current_user())
        case "su":
            su(params[0])
        case "chown":
            chown(params[0], params[1])
        case "permod":
            permod(params[0], params[1])
        case "list":
            list()
        case "goto":
            if params:
                goto(params[0])
            else:
                print("Ошибка: укажите директорию")
        case "mo":
            mo(params)
        case "co":
            co(params)
        case "rm":
            rm(params)
        case "make":
            make(params)
        case "fear":
            fear(params)
        case "find":
            find(params)
        case "sysfetch":
            sysfetch()
        case "help":
            help()
        case "exit":
            exit()
        case "clr":
            clr()
        case "owl":
            owl()
        case _:
            print("Unknown command. Type 'help' for a list of commands")
