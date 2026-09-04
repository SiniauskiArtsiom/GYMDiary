import streamlit as st
import requests
import os
API_URL = os.getenv("API_URL")

def create_set(exercise_id: int, order: int, weight: float, reps: int):
    payload = {
        "exercise_id": exercise_id,
        "order": order,
        "weight": weight,
        "reps": reps
    }
    try:
        response = requests.post(f"{API_URL}/sets/", json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Ошибка при создании подхода: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return None

def get_set_by_id(set_id: int):
    try:
        response = requests.get(f"{API_URL}/sets/{set_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке подхода: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return None


def get_sets_by_exercise(exercise_id: int):
    try:
        response = requests.get(f"{API_URL}/sets/by-exercise/{exercise_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке подходов: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return []


def delete_set(set_id: int) -> bool:
    try:
        response = requests.delete(f"{API_URL}/sets/{set_id}")
        if response.status_code == 204:
            return True
        else:
            st.error(f"Ошибка при удалении подхода: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к API: {e}")
        return False