import streamlit as st
import requests
import os
API_URL = os.getenv("API_URL")

def get_all_workouts():
    try:
        response = requests.get(f"{API_URL}/workouts/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке тренировок: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return []


def start_new_workout():
    try: 
        response = requests.post(f"{API_URL}/workouts/")
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Ошибка создания тренировки: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться к API: {e}")
            return None


def finish_workout(workout_id: int, calories_burned: int | None = None):
    payload = {"calories_burned": calories_burned} if calories_burned is not None else {}
    try:
        response = requests.post(f"{API_URL}/workouts/{workout_id}/finish", json = payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка завершения тренировки: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
                st.error(f"Не удалось подключиться к API: {e}")
                return None


def get_workout_by_id(workout_id: int):
    try:
        response = requests.get(f"{API_URL}/workouts/{workout_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке тренировки: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return None


def delete_workout_by_id(workout_id: int) -> bool:
    try:
        response = requests.delete(f"{API_URL}/workouts/{workout_id}")
        if response.status_code == 204:
            return True
        else:
            st.error(f"Ошибка при удалении тренировки: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return False