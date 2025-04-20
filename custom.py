commands_dict = {}  # Храним кастомные команды
variables = {}  # Глобальные переменные


def define_coma(command_name, command_body):
    """ Создаёт кастомную команду """
    commands_dict[command_name] = command_body


def remove_coma(command_name):
    """ Удаляет кастомную команду """
    if command_name in commands_dict:
        del commands_dict[command_name]


def set_variable(name, value):
    """Устанавливает переменную"""
    variables[name] = value


def get_variable(name):
    """Получает значение переменной"""
    return variables.get(name, f"*{name}*")  # Если нет, возвращает как есть
