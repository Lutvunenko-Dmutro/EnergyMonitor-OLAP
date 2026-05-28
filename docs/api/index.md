# 📚 Автоматичний API Референс

Ця сторінка автоматично збирає технічну документацію безпосередньо з вихідного коду (з `docstrings`) за допомогою плагіна `mkdocstrings`. 

!!! tip "Навігація та Пошук"
    Цей розділ ідеально підходить для розробників. Усі функції та класи автоматично індексуються, тому ви можете знайти будь-який метод системи через загальний рядок пошуку MkDocs (угорі сторінки).

---

## ⚙️ Ядро та Розрахунки (Core)
Фундаментальні розрахунки та взаємодія з локальною базою даних.

### Фізична модель (`physics.py`)
::: src.core.physics
    options:
      show_source: true
      heading_level: 4

### Менеджер БД (`database.py`)
::: src.core.database
    options:
      show_source: true
      heading_level: 4

---

## 🧠 Машинне навчання (ML)
Пайплайн препроцесингу та інференсу ШІ.

### Векторизатор (`vectorizer.py`)
::: src.ml.vectorizer
    options:
      show_source: true
      heading_level: 4

### LSTM Модель (`predict_v2.py`)
::: src.ml.predict_v2
    options:
      show_source: true
      heading_level: 4

---

## 🛠️ Сервіси (Services)
Фонові процеси, симуляція та цифрові двійники.

### Цифровий Двійник (`sensors_db.py`)
::: src.services.simulation.sensors_db
    options:
      show_source: true
      heading_level: 4

---

## 🔧 Утиліти (Utils)
Допоміжні інструменти для роботи системи.

### Загальні хелпери (`helpers.py`)
::: src.utils.helpers
    options:
      show_source: true
      heading_level: 4

### Кеш Менеджер (`cache_manager.py`)
::: src.utils.cache_manager
    options:
      show_source: true
      heading_level: 4