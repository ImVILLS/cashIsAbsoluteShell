import psutil


def list_processes():
    """ Показывает все процессы """
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        print(f"{proc.info['pid']} - {proc.info['name']}")


def kill_process(pid):
    """ Завершает процесс по PID """
    try:
        psutil.Process(pid).terminate()
        print(f"Процесс {pid} завершён.")
    except psutil.NoSuchProcess:
        print("Ошибка: процесс не найден.")
