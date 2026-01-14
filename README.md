<div align="center">

# 🏋️ Fitness RAG System

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)](https://python.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.22-purple?style=flat-square&logo=chromadb)](https://www.trychroma.com/)
[![RAG](https://img.shields.io/badge/RAG-Enabled-green?style=flat-square&logo=openai)](https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore)
[![Sentence--Transformers](https://img.shields.io/badge/Sentence--Transformers-2.2.2-red?style=flat-square&logo=huggingface)](https://www.sbert.net/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![Week--Program](https://img.shields.io/badge/4--Week--Program-168--Plans-orange?style=flat-square&logo=calendar)](https://github.com/)

**Персональный фитнес-тренер на базе RAG с ChromaDB**

*Генерирует индивидуальные планы тренировок на 4 недели*

[Особенности](#-особенности-системы) • [Установка](#-установка) • [Использование](#-использование-rag-системы) • [JSON API](#-использование-json-данных-в-других-проектах)

</div>

---

## 📁 Структура проекта

    fitness_rag_generator/  
    ├── fitness_rag_generator.py  # 📦 Генератор данных (создаёт JSON)
    ├── fitness_rag.py            # 🔍 RAG система (ChromaDB + поиск)
    ├── requirements.txt          # 📋 Зависимости
    ├── LICENSE                   # 📄 Лицензия
    ├── README.md                 # 📖 Этот файл
    └── .gitignore

    fitness_rag_data/             # 📂 Создаётся автоматически (generator)
    ├── exercises_library.json    # 💪 250+ упражнений с ASCII-схемами
    ├── warmup_routine.json       # 🏃 Разминка 5 минут
    ├── workout_plans_full.json   # 📅 168 тренировочных планов
    ├── muscle_groups.json        # 🏋️ Группы мышц
    ├── equipment_list.json       # 🛠️ Оборудование
    └── chromadb_metadata.json    # 📊 Метаданные для ChromaDB

    fitness_chroma_db/            # 🗄️ Создаётся автоматически (RAG)
    ├── exercises/                # Коллекция упражнений
    ├── workout_plans/            # Коллекция планов
    └── warmup/                   # Коллекция разминки

---

## 🔍 Что такое RAG система

**RAG** (Retrieval-Augmented Generation) — архитектура с 3 этапами:

RAG SYSTEM
═══════════════════════════════════════════════════════

  1️⃣  RETRIEVAL (Извлечение)
       Поиск релевантных данных в векторной базе
           │
           ▼
  2️⃣  AUGMENTATION (Дополнение)
       Добавление контекста к запросу
           │
           ▼
  3️⃣  GENERATION (Генерация)
       Формирование ответа на основе найденного

### В нашем проекте:

    # fitness_rag.py — это RAG система с 3 коллекциями:
    
    collections = {
        "exercises":    # 💪 250+ упражнений с ASCII-схемами
        "workout_plans": # 📅 168 планов (6 кат. × 4 нед. × 7 дн.)
        "warmup":        # 🏃 Разминка 5 минут
    }
    
    # SentenceTransformer (all-MiniLM-L6-v2) преобразует текст в векторы
    # ChromaDB хранит векторы и выполняет семантический поиск

---

## 👥 Поддерживаемые категории

| Категория | Описание |
|-----------|----------|
| `male_18_30` | Мужчины 18-30 лет |
| `male_26_45` | Мужчины 26-45 лет |
| `male_46_60` | Мужчины 46-60 лет |
| `female_18_30` | Женщины 18-30 лет |
| `female_26_45` | Женщины 26-45 лет |
| `female_46_60` | Женщины 46-60 лет |

---

## 🏋️ Группы мышц

- **Грудь** (Chest)
- **Спина** (Back)
- **Ноги** (Legs)
- **Плечи** (Shoulders)
- **Бицепс** (Biceps)
- **Трицепс** (Triceps)
- **Кор/Пресс** (минимальная нагрузка)

---

## 📋 Установка

```bash
    # 1. Перейди в папку проекта
    cd fitness_rag_generator

    # 2. Создай виртуальное окружение
    python -m venv venv

    # 3. Активируй его
    # Windows:
    venv\Scripts\activate
    # Linux/macOS:
    source venv/bin/activate

    # 4. Установи зависимости
    pip install -r requirements.txt
```

---

## 🚀 Запуск

### Шаг 1: Создание данных (генератор JSON)
```bash
    python fitness_rag_generator.py
```

Создаёт JSON файлы в `fitness_rag_data/`:
- 250+ упражнений с ASCII-схемами
- Разминка 5 минут (8 упражнений)
- 168 тренировочных планов (6 кат. × 4 нед. × 7 дн.)

### Шаг 2: Запуск RAG системы
```bash
    python fitness_rag.py
```

Загружает данные в ChromaDB и запускает интерактивный режим.

---

## 📖 Использование RAG системы

### Пример 1: Инициализация RAG
```bash
    from fitness_rag import FitnessRAGSystem

    # Инициализация (загружает данные в ChromaDB)
    rag = FitnessRAGSystem()
```

### Пример 2: Получить разминку
```bash
    warmup = rag.get_warmup()
    print(warmup['documents'][0])
```

### Пример 3: Поиск упражнений
```bash
    # Семантический поиск по запросу
    results = rag.search_exercises(
        "упражнения для груди без оборудования", 
        n_results=5
    )

    for ex in results['metadatas'][0]:
        print(f"{ex['name']} (сложность: {ex['difficulty']})")
```

### Пример 4: Получить план тренировки
```bash
    # Получить план для мужчины 18-30, неделя 1, день 1
    plan = rag.get_workout_plan("male", "18-30", 1, 1)

    for exercise in plan['metadatas'][0]:
        print(f"Неделя {exercise['week']}, День {exercise['day']}")
        print(f"Интенсивность: {exercise['intensity_level']}")
```

### Пример 5: Поиск похожих планов
```bash
    # Семантический поиск планов
    results = rag.search_similar_plans(
        "легкая тренировка для новичка",
        n_results=3
    )

    for plan in results['metadatas'][0]:
        print(f"Интенсивность: {plan['intensity_level']}")
```

### Пример 6: Все планы категории
```bash
    # Получить все планы для мужчины 26-45
    plans = rag.get_plans_by_category("male", "26-45")
    print(f"Найдено планов: {len(plans['ids'])}")
```

---

## 🔧 Использование JSON данных в других проектах

JSON файлы в `fitness_rag_data/` можно использовать без ChromaDB.

### Загрузка упражнений
```bash
    import json

    with open("fitness_rag_data/exercises_library.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    exercises = data["exercises"]
    print(f"Всего упражнений: {data['count']}")

    # Найти все упражнения для груди
    chest_exercises = [
        ex for ex in exercises 
        if "chest" in ex["primary_muscles"]
    ]

    for ex in chest_exercises:
        print(f"{ex['name']} - сложность: {ex['difficulty']}")
```

```bash
### Загрузка разминки
    with open("fitness_rag_data/warmup_routine.json", "r", encoding="utf-8") as f:
        warmup = json.load(f)

    print(f"Разминка: {warmup['name']}")
    print(f"Длительность: {warmup['total_duration']} сек")

    for ex in warmup['exercises']:
        print(f"- {ex['name']} ({ex['duration']} сек)")
```

### Загрузка планов тренировок
```bash
    with open("fitness_rag_data/workout_plans_full.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    plans = data["plans"]
    print(f"Всего планов: {data['total_plans']}")

    # Получить конкретный план
    plan_key = "male_18_30_week1_day1"
    plan = plans[plan_key]

    print(f"План: {plan['name']}")
    print(f"Мышцы: {plan['target_muscles']}")

    for ex in plan['exercises']:
        print(f"- {ex['name']}: {ex['sets']} × {ex['reps']}")
```

### Загрузка справочников
```bash
    with open("fitness_rag_data/muscle_groups.json", "r") as f:
        muscles = json.load(f)

    with open("fitness_rag_data/equipment_list.json", "r") as f:
        equipment = json.load(f)

    print("Группы мышц:", muscles["muscle_groups"])
    print("Оборудование:", equipment["equipment"])
```

---

## 📊 Формат данных

### Упражнение (exercises_library.json)
```bash
    {
      "id": "ex_001",
      "name": "Классические отжимания",
      "description": "Упражнение для развития chest мышц.",
      "primary_muscles": ["chest"],
      "secondary_muscles": ["triceps", "shoulders"],
      "difficulty": 3,
      "equipment": ["none"],
      "age_suitability": ["18-30", "26-45", "46-60"],
      "gender_suitability": ["male", "female"],
      "ascii_schematic": ["Схема упражнения"],
      "tempo": "2-1-2",
      "breathing": "Выдох на усилии",
      "safety": "Держите спину прямой"
    }
```

### План тренировки (workout_plans_full.json)
```bash
    {
      "name": "Понедельник: Грудь и трицепс",
      "category": {
        "gender": "male",
        "age_group": "18-30"
      },
      "week": 1,
      "day": 1,
      "target_muscles": ["chest", "triceps"],
      "intensity_level": "low",
      "work_rest_ratio": "40/20",
      "circuits": 2,
      "total_time": "20 минут (5 разминка + 15 тренировка)",
      "exercises": [
        {
          "exercise_id": "ex_001",
          "name": "Классические отжимания",
          "sets": 2,
          "reps": "10-12",
          "rest": 20,
          "notes": "Сосредоточьтесь на технике"
        }
      ],
      "cooldown": "Растяжка мышц"
    }
```

```bash
### Разминка (warmup_routine.json)
    {
      "id": "warmup_001",
      "name": "Универсальная разминка 5 минут",
      "description": "Подготовка суставов и мышц",
      "total_duration": 300,
      "exercises": [
        {
          "name": "Ходьба на месте",
          "duration": 60,
          "purpose": "Разогрев тела"
        }
      ]
    }
```

---

## ⚙️ Интенсивность по неделям

| Неделя | Уровень | Подходы × Повторения | Отдых | Круги |
|--------|---------|---------------------|-------|-------|
| 1 | Низкий | 2 × 10-12 | 20 сек | 2 |
| 2 | Средний | 3 × 12-15 | 15 сек | 3 |
| 3 | Высокий | 3 × 15-18 | 10 сек | 3 |
| 4 | Очень высокий | 4 × 18-20 | 5 сек | 4 |

---

## 🎯 Особенности системы

| Особенность | Реализация |
|-------------|------------|
| ✅ Разминка | Отдельный модуль, 5 минут |
| ✅ Тренировки | 15 минут (без разминки) |
| ✅ Full Body | Все группы мышц за неделю |
| ✅ Без повторений | Упражнения не повторяются внутри недели |
| ✅ Прогрессия | Интенсивность растёт каждую неделю |
| ✅ Кор/пресс | Минимальная нагрузка |
| ✅ ASCII-схемы | Визуализация упражнений |
| ✅ 6 категорий | Разные возрасты и полы |

---

## 📂 ChromaDB структура

    fitness_chroma_db/
    ├── exercises/                    # 💪 250+ упражнений
    │   ├── data.parquet             # Документы
    │   ├── embeddings.parquet       # Векторы (768 измерений)
    │   └── metadata.parquet         # Метаданные
    │
    ├── workout_plans/               # 📅 168 планов
    │   ├── data.parquet
    │   ├── embeddings.parquet
    │   └── metadata.parquet
    │
    └── warmup/                      # 🏃 Разминка
        ├── data.parquet
        ├── embeddings.parquet
        └── metadata.parquet

Модель эмбеддингов: `all-MiniLM-L6-v2` (384 или 768 измерений)

---

## 🔌 Интеграция в другие проекты

### Вариант 1: Использовать только JSON
```bash
    # Простой способ — без ChromaDB
    import json

    with open("fitness_rag_data/exercises_library.json") as f:
        exercises = json.load(f)["exercises"]

    # Ваша логика поиска...
```

### Вариант 2: Использовать RAG систему
```bash
    # Скопируй fitness_rag.py в свой проект
    from fitness_rag import FitnessRAGSystem

    rag = FitnessRAGSystem()
    plans = rag.get_plans_by_category("male", "26-45")
```

### Вариант 3: Создать свою RAG систему
```bash
    import chromadb
    from sentence_transformers import SentenceTransformer

    # Загружаешь данные из JSON
    with open("fitness_rag_data/exercises_library.json") as f:
        exercises = json.load(f)["exercises"]

    # Создаёшь свою коллекцию
    client = chromadb.Client()
    collection = client.create_collection("my_exercises")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Добавляешь свои данные...
```

---

## ⚠️ Требования

- Python 3.8+
- 4 GB RAM (для ChromaDB и модели)
- ~500 MB диска (данные + эмбеддинги)

---

## 📄 Лицензия

MIT License — подробности в файле [LICENSE](LICENSE)

---

## 📞 Контакты

**Автор**: Ivan P
**Telegram**: [@nonoyessure](https://t.me/nonoyessure)

---

<div align="center">

**⭐ Ставь звезду, если проект полезен!**

Сделано с ❤️

</div>
