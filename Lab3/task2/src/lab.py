import os


def write_file(path, text):
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as file:
        file.write(text)


def copy_file(source, target):
    with os.fdopen(os.open(source, os.O_RDONLY), "rb") as file:
        data = file.read()
    descriptor = os.open(
        target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "wb") as file:
        file.write(data)


def run(source, folder, text):
    os.chdir(folder)
    copy = os.path.join(folder, "copy.txt")
    copy_file(source, copy)
    renamed = os.path.join(folder, "renamed.txt")
    os.rename(copy, renamed)
    nested = os.path.join(folder, "level1", "level2")
    os.makedirs(nested, exist_ok=True)
    moved = os.path.join(nested, "renamed.txt")
    if os.path.exists(moved):
        os.remove(moved)
    os.rename(renamed, moved)

    new = os.path.join(folder, "new.txt")
    write_file(new, text)
    target = os.path.join(nested, "moved_new.txt")
    if os.path.exists(target):
        os.remove(target)
    # Одновременно перемещаем и переименовываем.
    os.rename(new, target)

    for i in range(3):
        write_file(f"file_{i}.txt", str(i))
    print("Папка скрипта:", sorted(os.listdir(folder)))
    os.chdir(nested)
    print("Вложенная папка:", sorted(os.listdir()))
    os.chdir(folder)
    os.mkdir("empty")
    os.rmdir("empty")
    extra = os.path.join(folder, "extra", "inside")
    os.makedirs(extra, exist_ok=True)
    write_file(os.path.join(extra, "note.txt"), "Еще один файл")
    for current, directories, files in os.walk(folder):
        print("Папка:", current)
        print("Файлы:", sorted(files))
    return moved, target


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.abspath(os.path.join(
        folder, "..", "..", "task1", "src", "created.txt"))
    input_path = os.path.join(folder, "..", "txt", "input.txt")
    with os.fdopen(os.open(input_path, os.O_RDONLY),
                   "r", encoding="utf-8") as file:
        text = file.read()
    if not os.path.isfile(source):
        print("Сначала запустите Lab3/task1/src/lab.py")
    else:
        run(source, folder, text)
