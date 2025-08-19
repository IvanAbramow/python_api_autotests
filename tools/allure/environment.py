import platform
import sys

from config import settings


def create_allure_environment_file():
    """
    Создает файл environment.properties для Allure,
    включая настройки из config и информацию о платформе.
    """
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]

    items.append(f'python_version={sys.version}')
    items.append(f'os_name={platform.system()}')
    items.append(f'os_version={platform.release()}')
    items.append(f'os_arch={platform.machine()}')

    properties = '\n'.join(items)

    try:
        settings.allure_results_dir.mkdir(parents=True, exist_ok=True)

        with open(settings.allure_results_dir.joinpath('environment.properties'), 'w') as file:
            file.write(properties)
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
