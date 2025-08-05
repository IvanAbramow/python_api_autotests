from faker import Faker


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        self.faker = faker

    def random_text(self) -> str:
        """
        Генерирует случайный текст.

        :return: Случайный текст.
        """
        return self.faker.text()

    def generate_uuid(self) -> str:
        """
        Генерирует случайный UUID4.

        :return: Случайный UUID4.
        """

        return self.faker.uuid4()

    def generate_email(self, domain: str | None = None) -> str:
        """
        Генерирует случайный email.

        :return: Случайный email.
        """
        return self.faker.email(domain=domain)

    def sentence(self) -> str:
        """
        Генерирует случайное предложение.

        :return: Случайное предложение.
        """
        return self.faker.sentence()

    def generate_password(self) -> str:
        """
        Генерирует случайный пароль.

        :return: Случайный пароль.
        """
        return self.faker.password()

    def generate_last_name(self) -> str:
        """
        Генерирует случайную фамилию.

        :return: Случайная фамилия.
        """
        return self.faker.last_name()

    def generate_first_name(self) -> str:
        """
        Генерирует случайное имя.

        :return: Случайное имя.
        """
        return self.faker.first_name()

    def generate_middle_name(self) -> str:
        """
        Генерирует случайное отчество/среднее имя.

        :return: Случайное отчество.
        """
        return self.faker.first_name()

    def generate_random_integer(self, start: int = 1, end: int = 100) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        :param start: Начало диапазона (включительно).
        :param end: Конец диапазона (включительно).
        :return: Случайное целое число.
        """
        return self.faker.random_int(start, end)

fake = Fake(faker=Faker())