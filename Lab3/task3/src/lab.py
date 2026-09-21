import os
import platform
import psutil


def list_processes():
    processes = []
    for process in psutil.process_iter(["pid", "name"]):
        processes.append(process.info)
    return processes


def process_info(pid):
    process = psutil.Process(pid)
    return process.as_dict(attrs=[
        "pid",
        "name",
        "username",
        "status",
        "create_time",
        "nice"
    ])


def terminate_process(pid):
    process = psutil.Process(pid)
    process.terminate()


def set_environment(name, value):
    if not name or "=" in name or "\0" in name or "\0" in value:
        raise ValueError("Неверное имя или значение переменной")

    os.environ[name] = value


def change_priority(pid, level):
    levels = {
        "low": psutil.IDLE_PRIORITY_CLASS,
        "normal": psutil.NORMAL_PRIORITY_CLASS,
        "high": psutil.HIGH_PRIORITY_CLASS
    }

    if level not in levels:
        raise ValueError("Допустимо: low, normal, high")

    process = psutil.Process(pid)
    process.nice(levels[level])


def system_info():
    return {
        "Система": platform.system(),
        "Версия Windows": platform.release(),
        "Архитектура": platform.machine(),
        "Имя компьютера": platform.node(),
        "Логические процессоры": os.cpu_count(),
        "Текущая папка": os.getcwd(),
        "PID скрипта": os.getpid(),
        "Пользователь": os.environ.get("USERNAME", "неизвестно")
    }


def main():
    while True:
        print("\na — показать процессы")
        print("b — информация о процессе")
        print("c — завершить процесс")
        print("d — переменные окружения")
        print("e — изменить приоритет")
        print("f — информация о системе")
        print("g — выход")

        choice = input("Выбор: ").strip().lower()

        try:
            if choice == "a":
                for process in list_processes():
                    print(process["pid"], "-", process["name"])

            elif choice == "b":
                pid = int(input("PID: "))
                print(process_info(pid))

            elif choice == "c":
                pid = int(input("PID: "))
                terminate_process(pid)
                print("Процесс завершён")

            elif choice == "d":
                for key, value in sorted(os.environ.items()):
                    print(key, "=", value)

                name = input("Имя новой переменной (Enter — назад): ").strip()
                if name:
                    value = input("Значение: ")
                    set_environment(name, value)
                    print("Переменная добавлена для текущей программы")

            elif choice == "e":
                pid = int(input("PID: "))
                level = input("Приоритет low/normal/high: ").strip().lower()
                change_priority(pid, level)
                print("Приоритет изменён")

            elif choice == "f":
                for key, value in system_info().items():
                    print(key + ":", value)

            elif choice == "g":
                break

            else:
                print("Нет такого пункта")

        except psutil.AccessDenied:
            print("Ошибка: недостаточно прав. Попробуйте запустить программу от администратора")
        except psutil.NoSuchProcess:
            print("Ошибка: процесс с таким PID не найден")
        except ValueError as error:
            print("Ошибка:", error)
        except OSError as error:
            print("Системная ошибка:", error)


if __name__ == "__main__":
    if os.name != "nt":
        print("Эта версия задания предназначена для Windows")
    else:
        main()
