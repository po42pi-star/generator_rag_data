import chromadb
import json
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings


class FitnessRAGSystem:
    def __init__(self):
        # Инициализация ChromaDB (локально, без Docker!)
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./fitness_chroma_db"
        ))
        
        # Загружаем модель для эмбеддингов
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Создаем коллекции
        self.create_collections()
        
        # Загружаем данные
        self.load_data()

    def create_collections(self):
        """Создаем коллекции в ChromaDB"""
        self.collections = {
            "exercises": self.client.get_or_create_collection(
                name="exercises",
                metadata={"description": "Упражнения с ASCII-схемами"}
            ),
            "workout_plans": self.client.get_or_create_collection(
                name="workout_plans",
                metadata={"description": "Тренировочные планы на 4 недели"}
            ),
            "warmup": self.client.get_or_create_collection(
                name="warmup",
                metadata={"description": "Разминка 5 минут"}
            )
        }
        print("✓ Коллекции ChromaDB созданы")

    def load_data(self):
        """Загружаем данные из JSON файлов"""
        
        # 1. Загружаем РАЗМИНКУ
        print("Загрузка разминки...")
        with open("fitness_rag_data/warmup_routine.json", "r", encoding="utf-8") as f:
            warmup = json.load(f)
        
        warmup_text = f"""
        Разминка: {warmup['name']}
        Описание: {warmup['description']}
        Длительность: {warmup['total_duration']} секунд
        Упражнения: {', '.join([ex['name'] for ex in warmup['exercises']])}
        """
        
        self.collections["warmup"].add(
            documents=[warmup_text],
            metadatas=[{"type": "warmup", "duration": warmup['total_duration']}],
            ids=["warmup_001"]
        )
        print("✓ Разминка загружена в ChromaDB")

        # 2. Загружаем УПРАЖНЕНИЯ
        print("Загрузка упражнений...")
        with open("fitness_rag_data/exercises_library.json", "r", encoding="utf-8") as f:
            exercises_data = json.load(f)
        
        exercise_texts = []
        exercise_metadatas = []
        exercise_ids = []
        
        for exercise in exercises_data["exercises"]:
            text = f"""
            Упражнение: {exercise['name']}
            Описание: {exercise['description']}
            Основные мышцы: {', '.join(exercise['primary_muscles'])}
            Оборудование: {', '.join(exercise['equipment'])}
            Сложность: {exercise['difficulty']}/5
            """
            exercise_texts.append(text)
            exercise_metadatas.append({
                "id": exercise["id"],
                "name": exercise["name"],
                "muscles": json.dumps(exercise["primary_muscles"]),
                "equipment": json.dumps(exercise["equipment"]),
                "difficulty": exercise["difficulty"],
                "ascii": json.dumps(exercise.get("ascii_schematic", []))
            })
            exercise_ids.append(exercise["id"])
        
        # Генерируем эмбеддинги и добавляем
        exercise_embeddings = self.model.encode(exercise_texts).tolist()
        self.collections["exercises"].add(
            embeddings=exercise_embeddings,
            documents=exercise_texts,
            metadatas=exercise_metadatas,
            ids=exercise_ids
        )
        print(f"✓ Загружено {len(exercise_ids)} упражнений в ChromaDB")

        # 3. Загружаем ПЛАНЫ ТРЕНИРОВОК
        print("Загрузка тренировочных планов...")
        with open("fitness_rag_data/workout_plans_full.json", "r", encoding="utf-8") as f:
            plans_data = json.load(f)
        
        plan_texts = []
        plan_metadatas = []
        plan_ids = []
        
        for plan_key, plan in plans_data["plans"].items():
            exercises_names = [ex["name"] for ex in plan["exercises"]]
            text = f"""
            План: {plan['name']}
            Для: {plan['category']['gender']}, возраст {plan['category']['age_group']}
            Неделя: {plan['week']}, День: {plan['day']}
            Мышцы: {', '.join(plan['target_muscles'])}
            Интенсивность: {plan['intensity_level']}
            Упражнения: {', '.join(exercises_names)}
            """
            plan_texts.append(text)
            plan_metadatas.append({
                "key": plan_key,
                "gender": plan['category']['gender'],
                "age_group": plan['category']['age_group'],
                "week": plan["week"],
                "day": plan["day"],
                "muscles": json.dumps(plan["target_muscles"]),
                "intensity_level": plan["intensity_level"]
            })
            plan_ids.append(plan_key)
        
        # Генерируем эмбеддинги и добавляем планы
        plan_embeddings = self.model.encode(plan_texts).tolist()
        self.collections["workout_plans"].add(
            embeddings=plan_embeddings,
            documents=plan_texts,
            metadatas=plan_metadatas,
            ids=plan_ids
        )
        print(f"✓ Загружено {len(plan_ids)} тренировочных планов в ChromaDB")

    def get_warmup(self):
        """Получить разминку"""
        results = self.collections["warmup"].get(ids=["warmup_001"])
        return results

    def search_exercises(self, query, n_results=5):
        """Поиск упражнений по запросу"""
        query_embedding = self.model.encode([query]).tolist()
        results = self.collections["exercises"].query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

    def get_workout_plan(self, gender, age_group, week, day):
        """Получить конкретный план тренировки"""
        plan_key = f"{gender}_{age_group.replace('-', '_')}_week{week}_day{day}"
        results = self.collections["workout_plans"].get(ids=[plan_key])
        return results

    def search_similar_plans(self, query, n_results=3):
        """Поиск похожих планов по запросу"""
        query_embedding = self.model.encode([query]).tolist()
        results = self.collections["workout_plans"].query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

    def get_plans_by_category(self, gender, age_group):
        """Получить все планы для категории"""
        all_plans = self.collections["workout_plans"].get()
        
        # Фильтруем по категории
        filtered = {
            "documents": [],
            "metadatas": [],
            "ids": [],
            "embeddings": []
        }
        
        for i, meta in enumerate(all_plans["metadatas"]):
            if meta["gender"] == gender and meta["age_group"] == age_group:
                filtered["documents"].append(all_plans["documents"][i])
                filtered["metadatas"].append(meta)
                filtered["ids"].append(all_plans["ids"][i])
                if "embeddings" in all_plans:
                    filtered["embeddings"].append(all_plans["embeddings"][i])
        
        return filtered


# ИСПОЛЬЗОВАНИЕ
if __name__ == "__main__":
    print("Инициализация RAG системы с ChromaDB...")
    rag = FitnessRAGSystem()
    
    print("\n" + "="*50)
    print("✅ RAG СИСТЕМА ГОТОВА К РАБОТЕ!")
    print("="*50)
    
    # 1. Получаем разминку
    print("\n1️⃣ Разминка:")
    warmup = rag.get_warmup()
    print(f"   {warmup['documents'][0][:150]}...")
    
    # 2. Ищем упражнения
    print("\n2️⃣ Поиск упражнений для груди:")
    exercises = rag.search_exercises("упражнения для грудных мышц без оборудования", n_results=3)
    for i, ex in enumerate(exercises['metadatas'][0]):
        print(f"   {i+1}. {ex['name']} (сложность: {ex['difficulty']})")
    
    # 3. Получаем план
    print("\n3️⃣ План тренировки:")
    plan = rag.get_workout_plan("male", "18-30", 1, 1)
    if plan['metadatas']:
        meta = plan['metadatas'][0]
        print(f"   Пол: {meta['gender']}, Возраст: {meta['age_group']}")
        print(f"   Неделя {meta['week']}, День {meta['day']}")
    
    # 4. Поиск похожих планов
    print("\n4️⃣ Поиск планов для новичков:")
    similar = rag.search_similar_plans("легкая тренировка для начинающих", n_results=2)
    for i, meta in enumerate(similar['metadatas'][0]):
        print(f"   {i+1}. Интенсивность: {meta['intensity_level']}")