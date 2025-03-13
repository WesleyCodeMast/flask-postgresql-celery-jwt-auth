import os


def application_modules(black_list: list[str] = None) -> list[str]:
    if not black_list:
        black_list = ['__pycache__', 'core']

    modules = []

    for x in os.scandir(os.getcwd()):
        if not x.is_dir() or x.name in black_list:
            continue
        modules.append(x.name)

    return modules


__all__ = (
    'application_modules',
)
