import os
from datetime import datetime


def go_to_script():
    folder = os.path.dirname(os.path.abspath(__file__))
    print("Исходная директория:", os.getcwd())
    if os.getcwd() != folder:
        os.chdir(folder)
    return folder


def write_file(path, text):
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as file:
        file.write(text)


def file_info(path):
    info = os.stat(path)
    return {
        "size": info.st_size,
        "modified": info.st_mtime,
        "accessed": info.st_atime,
        "mode": info.st_mode & 0o777,
    }


def current_user():
    try:
        return os.getlogin()
    except OSError:
        name = os.environ.get("USERNAME") or os.environ.get("USER")
        if name:
            return name
        if hasattr(os, "getuid"):
            return f"UID {os.getuid()}"
        return "Имя пользователя недоступно"


def change_permissions(path):
    # На Windows chmod управляет флагом «только чтение».
    old_mode = file_info(path)["mode"]
    new_mode = old_mode & ~0o222
    os.chmod(path, new_mode)
    return old_mode, file_info(path)["mode"]


if __name__ == "__main__":
    folder = go_to_script()
    source = os.path.join(folder, "..", "txt", "input.txt")
    with os.fdopen(os.open(source, os.O_RDONLY),
                   "r", encoding="utf-8") as file:
        text = file.read()
    path = os.path.join(folder, "created.txt")
    if os.path.exists(path):
        os.chmod(path, 0o600)
    write_file(path, text)
    print("Файл существует:", os.path.isfile(path))
    info = file_info(path)
    print("Размер:", info["size"], "байт")
    for key in ["modified", "accessed"]:
        print(key, datetime.fromtimestamp(info[key]))
    print("Пользователь:", current_user())
    before, after = change_permissions(path)
    print("Права:", oct(before), "->", oct(after))
    print("Запись отключена:", after & 0o222 == 0)
