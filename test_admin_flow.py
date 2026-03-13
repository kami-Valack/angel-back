import requests
import random
import string

BASE_URL = "http://localhost:8000"

def random_email(prefix="admin"):
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{rand}@example.com"

def register_admin():
    url = f"{BASE_URL}/auth/register"
    email = random_email()
    payload = {
        "name": "Admin Teste",
        "email": email,
        "password": "admin123"
    }
    response = requests.post(url, json=payload)
    print("[REGISTER ADMIN] Status:", response.status_code)
    print("[REGISTER ADMIN] Response:", response.json())
    token = response.json().get("data", {}).get("token")
    return email, "admin123", token

def login_admin(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    print("[LOGIN ADMIN] Status:", response.status_code)
    print("[LOGIN ADMIN] Response:", response.json())
    token = response.json().get("data", {}).get("token")
    return token

def create_course(token):
    url = f"{BASE_URL}/admin/courses"
    payload = {
        "title": "Curso Admin Flow",
        "description": "Curso criado via admin flow",
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
    course_id = response.json().get("data", {}).get("course", {}).get("id")
    # Extrair apenas o número
    if course_id and isinstance(course_id, str) and course_id.startswith("crs_"):
        course_id = int(course_id.replace("crs_", ""))
    return course_id

def create_module(token, course_id):
    url = f"{BASE_URL}/admin/courses/{course_id}/modules"
    payload = {
        "title": "Módulo Admin Flow",
        "description": "Módulo criado via admin flow",
        "order": 1,
        "lessons": [
            {
                "title": "Lição Admin Flow",
                "description": "Lição criada via admin flow",
                "content": "Conteúdo da lição...",
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

if __name__ == "__main__":
    # Registrar e logar admin
    email, password, token = register_admin()
    if not token:
        token = login_admin(email, password)
    if token:
        course_id = create_course(token)
        if course_id:
            create_module(token, course_id)
