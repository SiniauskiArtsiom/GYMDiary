import streamlit as st
import pandas as pd
from datetime import datetime
from functionality.workouts import (
    get_all_workouts, start_new_workout, get_workout_by_id,
    finish_workout, delete_workout_by_id
)
from functionality.exercises import (
    get_exercises_by_workout, create_exercise, delete_exercise_by_id
)
from functionality.sets import (
    get_sets_by_exercise, create_set, delete_set
)

st.set_page_config(page_title="GYMDiary", layout="wide")
st.title("GYMDiary — твой личный тренировочный дневник")

# Функция форматирования даты/времени
def format_datetime(iso_str):
    """Преобразует ISO строку в человеко-читаемый формат (ДД.ММ.ГГГГ ЧЧ:ММ)."""
    if not iso_str:
        return "—"
    try:
        # Обрабатываем возможный суффикс Z (UTC)
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return iso_str  # если не удалось, возвращаем исходное

# Инициализация session_state
if "menu" not in st.session_state:
    st.session_state.menu = "Мои тренировки"
if "selected_workout_id" not in st.session_state:
    st.session_state.selected_workout_id = None
if "selected_exercise_id" not in st.session_state:
    st.session_state.selected_exercise_id = None

menu_options = ["Мои тренировки", "Новая тренировка", "Тренировка", "Завершить тренировку"]

def on_menu_change():
    st.session_state.menu = st.session_state.menu_widget

# Боковое меню с синхронизацией через session_state
st.sidebar.radio(
    "Навигация",
    menu_options,
    index=menu_options.index(st.session_state.menu),
    key="menu_widget",
    on_change=on_menu_change
)

menu = st.session_state.menu

# ------------------- Вкладка "Мои тренировки" -------------------
if menu == "Мои тренировки":
    st.header("Мои тренировки")
    workouts = get_all_workouts()
    if workouts:
        df = pd.DataFrame(workouts)
        df = df.rename(columns={
            "id": "Номер",
            "started_at": "Начало",
            "finished_at": "Конец",
            "calories_burned": "Потрачено калорий"
        })
        # Форматируем даты
        df["Начало"] = df["Начало"].apply(format_datetime)
        df["Конец"] = df["Конец"].apply(lambda x: format_datetime(x) if x else "—")
        st.dataframe(df, use_container_width=True)  # для новых версий: width='stretch'

        workout_ids = [w["id"] for w in workouts]
        selected_id = st.selectbox("Выберите тренировку", workout_ids)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Просмотреть 👁"):
                st.session_state.selected_workout_id = selected_id
                st.session_state.menu = "Тренировка"
                st.rerun()
        with col2:
            if st.button("Удалить 🗑", key=f"del_workout_{selected_id}"):
                if delete_workout_by_id(selected_id):
                    st.success("Тренировка удалена")
                    st.rerun()
    else:
        st.info("Тренировок пока нет. Пора подкачаться!")

# ------------------- Вкладка "Новая тренировка" -------------------
elif menu == "Новая тренировка":
    st.header("Начать тренировку")
    if st.button("Start"):
        new_workout = start_new_workout()
        if new_workout:
            st.success(f"Тренировка #{new_workout['id']} начата в {format_datetime(new_workout['started_at'])}")
            st.session_state.selected_workout_id = new_workout["id"]
            st.session_state.menu = "Тренировка"
            st.rerun()

# ------------------- Вкладка "Тренировка" -------------------
elif menu == "Тренировка":
    st.header("Управление тренировкой")
    workouts = get_all_workouts()
    if not workouts:
        st.warning("Нет доступных тренировок")
    else:
        # Выбор тренировки
        if (st.session_state.selected_workout_id is None or 
            st.session_state.selected_workout_id not in [w["id"] for w in workouts]):
            workout_ids = [w["id"] for w in workouts]
            selected_workout = st.selectbox(
                "Выберите тренировку",
                workout_ids,
                format_func=lambda x: f"Тренировка #{x}"
            )
            st.session_state.selected_workout_id = selected_workout
        else:
            selected_workout = st.session_state.selected_workout_id
            st.write(f"Выбрана тренировка #{selected_workout}")
            if st.button("Сменить тренировку"):
                st.session_state.selected_workout_id = None
                st.rerun()

        # Детали тренировки
        workout_detail = get_workout_by_id(selected_workout)
        if workout_detail:
            is_finished = workout_detail.get("finished_at") is not None

            st.subheader(f"Детали тренировки #{selected_workout}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Начало", format_datetime(workout_detail.get("started_at")))
            col2.metric("Окончание", 
                        format_datetime(workout_detail.get("finished_at")) if is_finished else "ещё не завершена")
            col3.metric("Калории", workout_detail.get("calories_burned", "—"))

            st.markdown("---")
            st.subheader("Упражнения")

            # Добавление упражнения (только для незавершённой тренировки)
            if not is_finished:
                # Загружаем упражнения, чтобы вычислить следующий порядок
                exercises = get_exercises_by_workout(selected_workout)
                next_order = max([ex['order'] for ex in exercises], default=0) + 1

                with st.form("add_exercise_form", clear_on_submit=True):
                    ex_name = st.text_input("Название упражнения")
                    ex_order = st.number_input("Порядок", min_value=1, value=next_order, step=1)
                    submitted = st.form_submit_button("Добавить упражнение ➕")
                    if submitted and ex_name:
                        new_ex = create_exercise(selected_workout, ex_name, ex_order)
                        if new_ex:
                            st.success("Упражнение добавлено")
                            st.rerun()
            else:
                exercises = get_exercises_by_workout(selected_workout)

            if exercises:
                for ex in exercises:
                    with st.expander(f"{ex['name']} ({ex['order']} по очереди)"):
                        # Удаление упражнения (разрешено даже для завершённой, если нужно)
                        if not is_finished:
                            if st.button("Удалить упражнение 🗑", key=f"del_ex_{ex['id']}"):
                                if delete_exercise_by_id(ex["id"]):
                                    st.success("Упражнение удалено")
                                    st.rerun()

                        # Подходы
                        sets = get_sets_by_exercise(ex["id"])
                        if sets:
                            df_sets = pd.DataFrame(sets)
                            df_sets = df_sets.rename(columns={
                                "id": "ID",
                                "order": "Подход",
                                "weight": "Вес",
                                "reps": "Повторений"
                            })
                            st.dataframe(df_sets[["Подход", "Вес", "Повторений"]], use_container_width=True)
                        else:
                            st.caption("Пора сделать первый подход" if not is_finished else "Подходов нет")

                        # Добавление подхода (только если тренировка не завершена)
                        if not is_finished:
                            next_set_order = max([s['order'] for s in sets], default=0) + 1
                            with st.form(f"add_set_form_{ex['id']}", clear_on_submit=True):
                                set_order = st.number_input("Номер подхода", min_value=1, value=next_set_order, step=1, key=f"order_{ex['id']}")
                                set_weight = st.number_input("Вес", min_value=0.0, value=0.0, step=0.5, key=f"weight_{ex['id']}")
                                set_reps = st.number_input("Повторений", min_value=0, value=0, step=1, key=f"reps_{ex['id']}")
                                add_set_submitted = st.form_submit_button("Добавить подход")
                                if add_set_submitted:
                                    new_set = create_set(ex["id"], set_order, set_weight, set_reps)
                                    if new_set:
                                        st.success("Подход добавлен")
                                        st.rerun()
            else:
                st.info("Пора сделать первое упражнение." if not is_finished else "Упражнений нет")

# ------------------- Вкладка "Завершить тренировку" -------------------
elif menu == "Завершить тренировку":
    st.header("Завершить тренировку")
    workouts = get_all_workouts()
    unfinished = [w for w in workouts if not w.get("finished_at")]
    if not unfinished:
        st.success("У вас нет незавершённых тренировок")
    else:
        workout_ids = [w["id"] for w in unfinished]
        selected_id = st.selectbox("Выберите тренировку для завершения", workout_ids,
                                   format_func=lambda x: f"Тренировка #{x}")
        calories = st.number_input("Сожжённые калории (опционально)", min_value=0, value=0, step=10)
        if st.button("Завершить тренировку"):
            result = finish_workout(selected_id, calories if calories > 0 else None)
            if result:
                st.success(f"Тренировка #{selected_id} завершена!")
                st.rerun()