import sys


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("Файл не найден")


def edit_file(filename):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            print("Введите текст (Ctrl+D для сохранения):")
            while True:
                try:
                    line = input()
                    f.write(line + "\n")
                except EOFError:
                    break
    except FileNotFoundError:
        print("Файл не найден")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: fear <файл> [-r|-e]")
        sys.exit(1)

    filename = sys.argv[1]
    flag = sys.argv[2]

    if flag == "-r":
        read_file(filename)
    elif flag == "-e":
        edit_file(filename)
    else:
        print("Ошибка: используйте -r (чтение) или -e (редактирование)")
