import requests
import random
import string

BASE_URL = "http://localhost:8000"

def random_email(prefix="user"):
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{rand}@example.com"

def test_register():
    url = f"{BASE_URL}/auth/register"
    payload = {
        "name": "João Teste",
        "email": "joao.teste@example.com",
        "password": "senha123"
    }
    response = requests.post(url, json=payload)
    print("[REGISTER] Status:", response.status_code)
    print("[REGISTER] Response:", response.json())
    return response.json().get("data", {}).get("token")

def test_login(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    print("[LOGIN] Status:", response.status_code)
    print("[LOGIN] Response:", response.json())
    return response.json().get("data", {}).get("token")

def test_update_avatar(token, user_id):
    url = f"{BASE_URL}/profile/{user_id}"
    payload = {
        "name": "João Teste",
        "bio": "Bio atualizada via teste",
        "avatar": "https://cdn.suaplataforma.com/avatars/novo-avatar-teste.jpg"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, json=payload, headers=headers)
    print("[UPDATE AVATAR] Status:", response.status_code)
    print("[UPDATE AVATAR] Response:", response.json())

def test_admin_login(email, password):
    return test_login(email, password)

def test_create_course(token):
    url = f"{BASE_URL}/admin/courses"
    payload = {
        "title": "Curso Teste API",
        "description": "Curso criado via teste automatizado",
        "category": "html",
        "level": "beginner",
        "thumbnail": "https://cdn.suaplataforma.com/cursos/html-thumb.jpg",
        "price": "free",
        "tags": ["html", "web", "frontend"],
        "published": True
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=headers)
    print("[CREATE COURSE] Status:", response.status_code)
    print("[CREATE COURSE] Response:", response.json())
    return response.json().get("data", {}).get("course", {}).get("id")

def test_create_module(token, course_id):
    url = f"{BASE_URL}/admin/courses/{course_id}/modules"
    payload = {
        "title": "Módulo Teste",
        "description": "Módulo criado via teste",
        "order": 1,
        "lessons": [
            {
                "title": "Lição Teste",
                "description": "Primeira lição do módulo de teste",
                "content": "Conteúdo da lição de teste...",
                "videoUrl": "https://cdn.suaplataforma.com/videos/intro-html.mp4",
                "duration": 300,
                "order": 1,
                "resources": [
                    {
                        "title": "Material de apoio",
                        "type": "pdf",
                        "url": "https://cdn.suaplataforma.com/resources/material1.pdf"
                    }
                ]
            }
        ]
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=headers)
    print("[CREATE MODULE] Status:", response.status_code)
    print("[CREATE MODULE] Response:", response.json())

def test_create_module_with_lesson_and_resource(token, course_id):
    url = f"{BASE_URL}/admin/courses/{course_id}/modules"
    payload = {
        "title": "Módulo Extra Teste",
        "description": "Módulo extra criado via teste",
        "order": 2,
        "lessons": [
            {
                "title": "Lição Extra Teste",
                "description": "Lição extra do módulo de teste",
                "content": "Conteúdo da lição extra...",
                "videoUrl": "https://cdn.suaplataforma.com/videos/extra-html.mp4",
                "duration": 200,
                "order": 1,
                "resources": [
                    {
                        "title": "Material extra",
                        "type": "pdf",
                        "url": "https://cdn.suaplataforma.com/resources/material-extra.pdf"
                    }
                ]
            }
        ]
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=headers)
    print("[CREATE MODULE EXTRA] Status:", response.status_code)
    print("[CREATE MODULE EXTRA] Response:", response.json())

def test_register_admin():
    url = f"{BASE_URL}/auth/register"
    email = random_email("admin")
    payload = {
        "name": "Admin Teste",
        "email": email,
        "password": "admin123"
    }
    response = requests.post(url, json=payload)
    print("[REGISTER ADMIN] Status:", response.status_code)
    print("[REGISTER ADMIN] Response:", response.json())
    return email, "admin123"

def extract_course_id(course_id_str):
    # Remove prefixo 'crs_' se existir
    if isinstance(course_id_str, str) and course_id_str.startswith("crs_"):
        return int(course_id_str.replace("crs_", ""))
    return int(course_id_str)

if __name__ == "__main__":
    # Teste de registro e login de usuário comum
    token = test_register() or test_login("joao.teste@example.com", "senha123")
    if token:
        # Supondo que o id do usuário seja 1 (ajuste conforme necessário)
        test_update_avatar(token, 1)
    # Registrar admin com e-mail aleatório e testar
    admin_email, admin_password = test_register_admin()
    admin_token = test_admin_login(admin_email, admin_password)
    if admin_token:
        course_id_str = test_create_course(admin_token)
        course_id = extract_course_id(course_id_str)
        if course_id:
            test_create_module(admin_token, course_id)
            test_create_module_with_lesson_and_resource(admin_token, course_id)
