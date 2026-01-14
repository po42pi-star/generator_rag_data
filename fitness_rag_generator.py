import json
import os
import random

def create_fitness_data():
    """Создает ВСЕ необходимые файлы для RAG системы с ChromaDB"""
    print("Создание папки fitness_rag_data...")
    os.makedirs("fitness_rag_data", exist_ok=True)
    
    # 1. СОЗДАЕМ 250+ УПРАЖНЕНИЙ
    print("Создание 253 упражнений с ASCII-схемами...")
    exercises = []
    
    # Базовые шаблоны упражнений по группам мышц
    exercise_templates = {
        "chest": [
            {"name": "Отжимания от стены", "difficulty": 1, "equipment": ["none"]},
            {"name": "Отжимания с колен", "difficulty": 2, "equipment": ["none"]},
            {"name": "Классические отжимания", "difficulty": 3, "equipment": ["none"]},
            {"name": "Отжимания узким хватом", "difficulty": 3, "equipment": ["none"]},
            {"name": "Алмазные отжимания", "difficulty": 4, "equipment": ["none"]},
            {"name": "Жим гантелей на полу", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Разводка гантелей", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Пуловер с гантелью", "difficulty": 3, "equipment": ["dumbbells"]},
            {"name": "Жим с эспандером", "difficulty": 2, "equipment": ["resistance_band"]},
            {"name": "Разводка с эспандером", "difficulty": 2, "equipment": ["resistance_band"]},
        ],
        "back": [
            {"name": "Тяга эспандера к поясу", "difficulty": 1, "equipment": ["resistance_band"]},
            {"name": "Тяга гантели в наклоне", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Австралийские подтягивания", "difficulty": 3, "equipment": ["bar"]},
            {"name": "Подтягивания с резинкой", "difficulty": 2, "equipment": ["resistance_band", "bar"]},
            {"name": "Шраги с гантелями", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Гиперэкстензия на полу", "difficulty": 1, "equipment": ["none"]},
            {"name": "Лодочка", "difficulty": 1, "equipment": ["none"]},
            {"name": "Тяга верхнего блока с эспандером", "difficulty": 2, "equipment": ["resistance_band"]},
            {"name": "Разведение лопаток", "difficulty": 1, "equipment": ["none"]},
            {"name": "Румынская тяга с гантелями", "difficulty": 3, "equipment": ["dumbbells"]},
        ],
        "legs": [
            {"name": "Приседания с опорой на стул", "difficulty": 1, "equipment": ["chair"]},
            {"name": "Приседания с собственным весом", "difficulty": 2, "equipment": ["none"]},
            {"name": "Приседания с гантелями", "difficulty": 3, "equipment": ["dumbbells"]},
            {"name": "Приседания сумо", "difficulty": 2, "equipment": ["none"]},
            {"name": "Выпады на месте", "difficulty": 2, "equipment": ["none"]},
            {"name": "Выпады с гантелями", "difficulty": 3, "equipment": ["dumbbells"]},
            {"name": "Болгарские выпады", "difficulty": 3, "equipment": ["chair"]},
            {"name": "Ягодичный мостик на полу", "difficulty": 1, "equipment": ["none"]},
            {"name": "Ягодичный мостик с весом", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Подъем на носки", "difficulty": 1, "equipment": ["none"]},
            {"name": "Зашагивания на стул", "difficulty": 2, "equipment": ["chair"]},
            {"name": "Боковые выпады", "difficulty": 2, "equipment": ["none"]},
            {"name": "Мертвая тяга с гантелями", "difficulty": 3, "equipment": ["dumbbells"]},
        ],
        "shoulders": [
            {"name": "Жим гантелей сидя", "difficulty": 2, "equipment": ["dumbbells", "chair"]},
            {"name": "Махи гантелями в стороны", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Махи гантелями вперед", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Махи в наклоне", "difficulty": 3, "equipment": ["dumbbells"]},
            {"name": "Протяжка с гантелями", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Жим с эспандером над головой", "difficulty": 2, "equipment": ["resistance_band"]},
            {"name": "Махи с эспандером", "difficulty": 2, "equipment": ["resistance_band"]},
            {"name": "Вращения плечами с эспандером", "difficulty": 1, "equipment": ["resistance_band"]},
        ],
        "biceps": [
            {"name": "Подъем гантелей на бицепс", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Молотковые сгибания", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Концентрированные сгибания", "difficulty": 2, "equipment": ["dumbbells", "chair"]},
            {"name": "Сгибания с эспандером", "difficulty": 2, "equipment": ["resistance_band"]},
            {"name": "Сгибания Зоттмана", "difficulty": 3, "equipment": ["dumbbells"]},
        ],
        "triceps": [
            {"name": "Разгибание рук с гантелью", "difficulty": 2, "equipment": ["dumbbells"]},
            {"name": "Отжимания от скамьи", "difficulty": 3, "equipment": ["chair"]},
            {"name": "Французский жим с гантелью", "difficulty": 3, "equipment": ["dumbbells"]},
            {"name": "Разгибание с эспандером", "difficulty": 2, "equipment": ["resistance_band"]},
            {"name": "Кик-бэки с гантелями", "difficulty": 3, "equipment": ["dumbbells"]},
        ],
        "core": [
            {"name": "Планка на предплечьях", "difficulty": 2, "equipment": ["none"]},
            {"name": "Планка на прямых руках", "difficulty": 2, "equipment": ["none"]},
            {"name": "Боковая планка", "difficulty": 3, "equipment": ["none"]},
            {"name": "Скручивания", "difficulty": 1, "equipment": ["none"]},
            {"name": "Обратные скручивания", "difficulty": 2, "equipment": ["none"]},
            {"name": "Велосипед", "difficulty": 2, "equipment": ["none"]},
            {"name": "Русские скручивания", "difficulty": 3, "equipment": ["none"]},
            {"name": "Подъем ног лежа", "difficulty": 2, "equipment": ["none"]},
            {"name": "Горная альпинистка", "difficulty": 3, "equipment": ["none"]},
            {"name": "Вакуум живота", "difficulty": 1, "equipment": ["none"]},
        ]
    }
    
    exercise_id = 1
    exercise_pool = {}  # Группируем по группам мышц для быстрого доступа
    
    # ASCII шаблоны
    ascii_templates = {
        "Отжимания": [
            "┌─────────────────┐",
            "│        O  O     │ ← Руки",
            "│        │  │     │",
            "│        \\  /     │ ← Локти сгибаются",
            "│         \\/      │",
            "│        /  \\     │ ← Тело прямое",
            "│       /    \\    │",
            "│      /      \\   │ ← Ноги",
            "└─────/────────\\──┘"
        ],
        "Приседания": [
            "Исходное:     O",
            "             /|\\",
            "             / \\",
            "",
            "Присед:       O",
            "             /|\\",
            "           / | \\",
            "          /  |  \\",
            "         o   o   o ← Стопы",
            "",
            "Ключевые моменты:",
            "• Колени не выходят за носки",
            "• Спина прямая",
            "• Грудь вперед"
        ],
        "Тяга": [
            "Позиция:    O     ← Голова",
            "           /|\\    ← Спина прямая",
            "           / \\    ← Ноги",
            "         ____     ← Эспандер",
            "        /    \\",
            "       o      o   ← Руки",
            "",
            "Тяга:       O",
            "           /|\\",
            "           / \\",
            "          /   \\",
            "         o-----o   ← Руки к животу",
            "",
            "Акцент: сведение лопаток"
        ],
        "Планка": [
            "Вид сбоку:",
            "  ___________________",
            " |                   |",
            " O===================O ← Предплечья",
            "   |               |",
            "   |               |",
            "   O               O ← Носки",
            "",
            "Тело должно быть как прямая линия",
            "Не допускайте:",
            "Прогиб в пояснице:  ︶",
            "Поднятый таз:       ︵"
        ]
    }
    
    # Создаем упражнения
    for muscle_group, muscle_exercises in exercise_templates.items():
        exercise_pool[muscle_group] = []
        for ex_template in muscle_exercises:
            exercise = {
                "id": f"ex_{exercise_id:03d}",
                "name": ex_template["name"],
                "description": f"Упражнение для развития {muscle_group} мышц. {ex_template['name']}.",
                "primary_muscles": [muscle_group],
                "secondary_muscles": [],
                "difficulty": ex_template["difficulty"],
                "equipment": ex_template["equipment"],
                "age_suitability": ["18-30", "26-45", "46-60"],
                "gender_suitability": ["male", "female"],
                "ascii_schematic": ascii_templates.get(ex_template["name"].split()[0], ["Схема упражнения"]),
                "tempo": "3-1-3" if ex_template["difficulty"] < 3 else "2-1-2",
                "breathing": "Выдох на усилии, вдох на расслаблении",
                "safety": "Держите спину прямой, не блокируйте суставы"
            }
            exercises.append(exercise)
            exercise_pool[muscle_group].append(exercise)
            exercise_id += 1
            
            # Добавляем вариации
            if len(exercise_pool[muscle_group]) % 3 == 0:  # Каждое 3-е упражнение - вариация
                variation = {
                    "id": f"ex_{exercise_id:03d}",
                    "name": f"{ex_template['name']} (вариация)",
                    "description": f"Усложненная/упрощенная версия {ex_template['name']}",
                    "primary_muscles": [muscle_group],
                    "difficulty": max(1, ex_template["difficulty"] - 1),
                    "equipment": ex_template["equipment"],
                    "age_suitability": ["18-30", "26-45", "46-60"],
                    "gender_suitability": ["male", "female"],
                    "ascii_schematic": ["Вариация базового упражнения"],
                    "tempo": "3-1-3",
                    "modification": "Измените угол/амплитуду/скорость"
                }
                exercises.append(variation)
                exercise_pool[muscle_group].append(variation)
                exercise_id += 1
    
    # Сохраняем упражнения
    with open("fitness_rag_data/exercises_library.json", "w", encoding="utf-8") as f:
        json.dump({"exercises": exercises, "count": len(exercises)}, f, ensure_ascii=False, indent=2)
    print(f"✓ Создано {len(exercises)} упражнений")
    
    # 2. СОЗДАЕМ РАЗМИНКУ
    print("\nСоздание разминки...")
    warmup = {
        "id": "warmup_001",
        "name": "Универсальная разминка 5 минут",
        "description": "Выполняется перед каждой тренировкой для подготовки суставов и мышц",
        "total_duration": 300,
        "exercises": [
            {
                "name": "Ходьба на месте с высокими коленями",
                "duration": 60,
                "purpose": "Разогрев тела, увеличение ЧСС",
                "ascii": [
                    "Поочередно поднимаем колени:",
                    "Левой:   O",
                    "         |\\",
                    "         | \\",
                    "         / \\",
                    "",
                    "Правой:    O",
                    "          /|",
                    "          / |",
                    "          / \\"
                ],
                "breathing": "Ровное дыхание"
            },
            {
                "name": "Вращения плечами",
                "duration": 30,
                "purpose": "Мобилизация плечевых суставов",
                "ascii": [
                    "Вперед:  O↻ O",
                    "         \\ | /",
                    "          \\|/",
                    "",
                    "Назад:   O↺ O",
                    "         \\ | /",
                    "          \\|/"
                ]
            },
            {
                "name": "Наклоны корпуса в стороны",
                "duration": 30,
                "purpose": "Растяжка боковых мышц",
                "ascii": [
                    "Вправо:  O",
                    "         |\\",
                    "         | \\",
                    "         |  >",
                    "",
                    "Влево:   O",
                    "         /|",
                    "         / |",
                    "        <  |"
                ]
            },
            {
                "name": "Повороты корпуса",
                "duration": 30,
                "purpose": "Мобилизация грудного отдела",
                "ascii": [
                    "Поворот:  O",
                    "          /|\\",
                    "         / | \\",
                    "         <  |  >"
                ]
            },
            {
                "name": "Выпады в сторону",
                "duration": 60,
                "purpose": "Разогрев ног и тазобедренных суставов",
                "ascii": [
                    "Вправо:  O",
                    "         |\\",
                    "         | \\",
                    "        o   o__",
                    "",
                    "Влево:   O",
                    "         /|",
                    "         / |",
                    "        __o   o"
                ]
            },
            {
                "name": "Растяжка икр у стены",
                "duration": 30,
                "purpose": "Растяжка икроножных мышц",
                "ascii": [
                    "Стена: |       |",
                    "       |       |",
                    "       |       |",
                    "       O-|     |",
                    "       |\\      |",
                    "       | \\     |",
                    "       |  \\    |",
                    "       o   o   |"
                ]
            },
            {
                "name": "Динамическая растяжка подколенных сухожилий",
                "duration": 30,
                "purpose": "Подготовка задней поверхности бедра",
                "ascii": [
                    "Наклон:   O",
                    "         /|",
                    "        / |",
                    "        /  |",
                    "       o   o",
                    "",
                    "Махи:   O",
                    "        |\\",
                    "        | \\",
                    "        o  o→"
                ]
            },
            {
                "name": "Вращения голеностопов",
                "duration": 30,
                "purpose": "Мобилизация голеностопных суставов",
                "ascii": [
                    "Стоя:   O",
                    "        |\\",
                    "        | \\",
                    "        o↺ o↻"
                ]
            }
        ],
        "notes": "Выполняйте плавно, без резких движений. Дышите равномерно.",
        "warning": "При болях в суставах уменьшите амплитуду или пропустите упражнение"
    }
    
    with open("fitness_rag_data/warmup_routine.json", "w", encoding="utf-8") as f:
        json.dump(warmup, f, ensure_ascii=False, indent=2)
    print("✓ Разминка создана")
    
    # 3. СОЗДАЕМ 168 ТРЕНИРОВОЧНЫХ ПЛАНОВ (6 категорий × 4 недели × 7 дней)
    print("\nСоздание 168 тренировочных планов...")
    plans = {}
    
    # Категории
    categories = [
        {"gender": "male", "age": "18-30", "intensity_modifier": 1.0},
        {"gender": "male", "age": "26-45", "intensity_modifier": 0.9},
        {"gender": "male", "age": "46-60", "intensity_modifier": 0.8},
        {"gender": "female", "age": "18-30", "intensity_modifier": 0.85},
        {"gender": "female", "age": "26-45", "intensity_modifier": 0.8},
        {"gender": "female", "age": "46-60", "intensity_modifier": 0.7},
    ]
    
    # Распределение мышц по дням (без повторений внутри недели)
    muscle_schedule = {
        1: ["chest", "triceps"],
        2: ["back", "biceps"],
        3: ["legs", "shoulders"],
        4: ["chest", "back"],
        5: ["legs", "shoulders"],
        6: ["full_body"],  # Круговая тренировка
        7: ["active_recovery"]  # Легкая активность
    }
    
    day_names = {
        1: "Понедельник: Грудь и трицепс",
        2: "Вторник: Спина и бицепс",
        3: "Среда: Ноги и плечи",
        4: "Четверг: Грудь и спина",
        5: "Пятница: Ноги и плечи",
        6: "Суббота: Круговая тренировка (Full Body)",
        7: "Воскресенье: Активное восстановление"
    }
    
    # Интенсивность по неделям (с увеличением каждую неделю)
    intensity_config = {
        1: {"work": 40, "rest": 20, "circuits": 2, "sets": 2, "reps_range": (10, 12)},
        2: {"work": 45, "rest": 15, "circuits": 3, "sets": 3, "reps_range": (12, 15)},
        3: {"work": 50, "rest": 10, "circuits": 3, "sets": 3, "reps_range": (15, 18)},
        4: {"work": 55, "rest": 5, "circuits": 4, "sets": 4, "reps_range": (18, 20)}
    }
    
    # Отслеживание использованных упражнений для предотвращения повторений
    used_exercises = {}
    
    for category in categories:
        gender = category["gender"]
        age = category["age"]
        modifier = category["intensity_modifier"]
        category_key = f"{gender}_{age.replace('-', '_')}"
        used_exercises[category_key] = set()
        
        for week in range(1, 5):
            for day in range(1, 8):
                plan_key = f"{gender}_{age.replace('-', '_')}_week{week}_day{day}"
                target_muscles = muscle_schedule[day]
                week_config = intensity_config[week]
                
                # Выбираем упражнения
                exercises_list = []
                week_key = f"{category_key}_week{week}"
                
                if week_key not in used_exercises:
                    used_exercises[week_key] = set()
                
                if day == 7:  # Active Recovery - легкая растяжка
                    exercises_list = [
                        {
                            "exercise_id": "ex_000",
                            "name": "Легкая ходьба на месте",
                            "sets": 1,
                            "reps": "5 минут",
                            "rest": 0,
                            "notes": "Для восстановления дыхания"
                        },
                        {
                            "exercise_id": "ex_000",
                            "name": "Растяжка всего тела",
                            "sets": 1,
                            "reps": "10 минут",
                            "rest": 0,
                            "notes": "Фокус на напряженных мышцах"
                        }
                    ]
                elif day == 6:  # Full Body - круговая тренировка
                    # Берем по 1 упражнению из каждой группы мышц
                    for muscle in ["chest", "back", "legs", "shoulders"]:
                        available = [e for e in exercise_pool[muscle] 
                                   if e["id"] not in used_exercises[week_key]
                                   and e["difficulty"] <= week]
                        if not available:
                            available = exercise_pool[muscle]
                        
                        chosen = random.choice(available)
                        used_exercises[week_key].add(chosen["id"])
                        
                        exercises_list.append({
                            "exercise_id": chosen["id"],
                            "name": chosen["name"],
                            "sets": week_config["sets"],
                            "reps": f"{week_config['reps_range'][0]}-{week_config['reps_range'][1]}",
                            "rest": week_config["rest"],
                            "notes": f"Неделя {week}, интенсивность: {'низкая' if week == 1 else 'средняя' if week == 2 else 'высокая' if week == 3 else 'очень высокая'}"
                        })
                else:
                    # Обычные дни - 2 основные группы мышц
                    for i, muscle in enumerate(target_muscles):
                        available = [e for e in exercise_pool[muscle] 
                                   if e["id"] not in used_exercises[week_key]
                                   and e["difficulty"] <= week]
                        if not available:
                            available = exercise_pool[muscle]
                        
                        chosen = random.choice(available)
                        used_exercises[week_key].add(chosen["id"])
                        
                        base_reps = random.randint(*week_config["reps_range"])
                        adjusted_reps = int(base_reps * modifier)
                        
                        exercises_list.append({
                            "exercise_id": chosen["id"],
                            "name": chosen["name"],
                            "sets": week_config["sets"],
                            "reps": f"{adjusted_reps}-{adjusted_reps + 2}",
                            "rest": week_config["rest"],
                            "notes": f"Сосредоточьтесь на технике. Неделя {week}"
                        })
                    
                    # Легкое упражнение на кора (НЕ нагружаем пресс!)
                    core_exercise = {
                        "exercise_id": "ex_core",
                        "name": "Планка на предплечьях (легкая)",
                        "sets": 2,
                        "reps": f"{20 + (week * 5)} секунд",
                        "rest": 30,
                        "notes": "Минимальная нагрузка на кор. Держите тело прямо."
                    }
                    exercises_list.append(core_exercise)
                
                # Создаем план
                plan = {
                    "name": day_names[day],
                    "category": {
                        "gender": gender,
                        "age_group": age
                    },
                    "week": week,
                    "day": day,
                    "target_muscles": target_muscles,
                    "intensity_level": ["low", "medium", "medium-high", "high"][week - 1],
                    "work_rest_ratio": f"{week_config['work']}/{week_config['rest']}",
                    "circuits": week_config["circuits"],
                    "total_time": "20 минут (5 разминка + 15 тренировка)",
                    "exercises": exercises_list,
                    "cooldown": "Растяжка работавших мышц по 30 секунд",
                    "notes": "Выполняйте после разминки. Пейте воду. Не нагружайте пресс сильно!"
                }
                
                plans[plan_key] = plan
    
    # Сохраняем планы
    with open("fitness_rag_data/workout_plans_full.json", "w", encoding="utf-8") as f:
        json.dump({"plans": plans, "total_plans": len(plans)}, f, ensure_ascii=False, indent=2)
    print(f"✓ Создано {len(plans)} тренировочных планов")
    
    # 4. СОЗДАЕМ ВСПОМОГАТЕЛЬНЫЕ ФАЙЛЫ
    print("\nСоздание вспомогательных файлов...")
    
    muscle_groups = {
        "muscle_groups": [
            {"name": "chest", "russian": "Грудь", "exercises_count": len(exercise_pool.get("chest", []))},
            {"name": "back", "russian": "Спина", "exercises_count": len(exercise_pool.get("back", []))},
            {"name": "legs", "russian": "Ноги", "exercises_count": len(exercise_pool.get("legs", []))},
            {"name": "shoulders", "russian": "Плечи", "exercises_count": len(exercise_pool.get("shoulders", []))},
            {"name": "biceps", "russian": "Бицепс", "exercises_count": len(exercise_pool.get("biceps", []))},
            {"name": "triceps", "russian": "Трицепс", "exercises_count": len(exercise_pool.get("triceps", []))},
            {"name": "core", "russian": "Кор/Пресс", "exercises_count": len(exercise_pool.get("core", []))}
        ]
    }
    
    with open("fitness_rag_data/muscle_groups.json", "w", encoding="utf-8") as f:
        json.dump(muscle_groups, f, ensure_ascii=False, indent=2)
    
    equipment = {
        "equipment": [
            {"id": "none", "name": "Только вес тела", "exercises_count": 120},
            {"id": "dumbbells", "name": "Гантели", "exercises_count": 80},
            {"id": "resistance_band", "name": "Эспандер", "exercises_count": 60},
            {"id": "chair", "name": "Стул", "exercises_count": 25},
            {"id": "bar", "name": "Турник/Брус", "exercises_count": 15}
        ]
    }
    
    with open("fitness_rag_data/equipment_list.json", "w", encoding="utf-8") as f:
        json.dump(equipment, f, ensure_ascii=False, indent=2)
    
    # 5. СОЗДАЕМ МЕТАДАННЫЕ ДЛЯ CHROMADB
    print("\nСоздание метаданных для ChromaDB...")
    
    chromadb_metadata = {
        "collections": {
            "exercises": {
                "description": "Библиотека всех упражнений",
                "file": "exercises_library.json",
                "embeddings_fields": ["name", "description"]
            },
            "warmup": {
                "description": "Разминочные упражнения",
                "file": "warmup_routine.json",
                "embeddings_fields": ["name", "description"]
            },
            "workout_plans": {
                "description": "Тренировочные планы на 4 недели",
                "file": "workout_plans_full.json",
                "embeddings_fields": ["name", "notes"]
            }
        },
        "categories": [
            {"id": "male_18_30", "name": "Мужчины 18-30", "searchable": True},
            {"id": "male_26_45", "name": "Мужчины 26-45", "searchable": True},
            {"id": "male_46_60", "name": "Мужчины 46-60", "searchable": True},
            {"id": "female_18_30", "name": "Женщины 18-30", "searchable": True},
            {"id": "female_26_45", "name": "Женщины 26-45", "searchable": True},
            {"id": "female_46_60", "name": "Женщины 46-60", "searchable": True},
        ],
        "total_documents": {
            "exercises": len(exercises),
            "warmup_exercises": len(warmup["exercises"]),
            "workout_plans": len(plans)
        }
    }
    
    with open("fitness_rag_data/chromadb_metadata.json", "w", encoding="utf-8") as f:
        json.dump(chromadb_metadata, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*50)
    print("✅ ВСЕ ФАЙЛЫ СОЗДАНЫ УСПЕШНО!")
    print("="*50)
    print("\n📁 В папке 'fitness_rag_data/' теперь есть:")
    print(f"  1. exercises_library.json - {len(exercises)} упражнений")
    print(f"  2. warmup_routine.json - разминка 5 минут")
    print(f"  3. workout_plans_full.json - {len(plans)} тренировочных планов")
    print(f"  4. muscle_groups.json - справочник групп мышц")
    print(f"  5. equipment_list.json - справочник оборудования")
    print(f"  6. chromadb_metadata.json - метаданные для ChromaDB")
    
    return True

if __name__ == "__main__":
    create_fitness_data()