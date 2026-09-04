import streamlit as st
import requests

import os
API_URL = os.getenv("API_URL")


def create_exercise(workout_id: int, name: str, order: int):
    payload = {
        "workout_id": workout_id,
        "name": name,
        "order": order
    }
    try:
        response = requests.post(f"{API_URL}/exercises/", json = payload)
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Ошибка создания упражнения: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться к API: {e}")
            return []


def get_exercise_with_sets(exercise_id: int):
    try:
        response = requests.get(f"{API_URL}/exercises/{exercise_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке упражнения: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return None


def get_exercises_by_workout(workout_id: int):
    try:
        response = requests.get(f"{API_URL}/exercises/by-workout/{workout_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке упражнений: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return []


def delete_exercise_by_id(exercise_id: int) -> bool:
    try:
        response = requests.delete(f"{API_URL}/exercises/{exercise_id}")
        if response.status_code == 204:
            return True
        else:
            st.error(f"Ошибка при удалении упражнения: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return False