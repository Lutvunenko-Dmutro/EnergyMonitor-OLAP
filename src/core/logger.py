import logging
import sys


def setup_logger(module_name):
    """
    Налаштовує глобальний логер для проєкту.
    Пише логи і в консоль, і у файл system.log.
    """
    logger = logging.getLogger(module_name)

    # Запобігаємо дублюванню логів у Streamlit (бо він часто перезапускає скрипти)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="[%(asctime)s] ⚡ %(levelname)-5s | %(name)s -> %(message)s",
            datefmt="%H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.propagate = False

        # 2. Вивід у файл (історія)
        file_handler = logging.FileHandler("system.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Глушимо зайвий спам від інших бібліотек (наприклад, Streamlit чи SQLAlchemy)
        logging.getLogger("streamlit").setLevel(logging.ERROR)
        logging.getLogger("PIL").setLevel(logging.WARNING)

    return logger
