# ATLAS_PASSPORT: docs/system/map/app_core_logic.md
from enum import Enum
"""
ГЛОБАЛЬНИЙ РЕЄСТР КОНФІГУРАЦІЙ (Global Config Registry)
======================================================
Централізоване сховище констант та ключів доступу до даних. 
Визначає структуру словників стану (State Dictionaries), що використовуються 
для обміну інформацією між Core Analytics та UI-компонентами.
"""
class DataKeys:
    """
    Ключі для доступу до словників даних та константи фільтрації.
    """

    LOAD = "load"
    GEN = "gen"
    ALERTS = "alerts"
    LINES = "lines"
    FINANCE = "fin"
    ALL_REGIONS = "Всі регіони"
