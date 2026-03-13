import jwt

# Chave secreta para JWT (use uma chave forte em produção)
JWT_SECRET = "sua_chave_secreta"
JWT_ALGORITHM = "HS256"
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql
import hashlib
from typing import Optional, List, Dict

def success_response(message: str, data: dict = None, status_code: int = 200):
    return {
        "success": True,
        "message": message,
        "data": data or {}
    }

def error_response(code: str, message: str, status_code: int = 400, details: list = None):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            **({"details": details} if details else {})
        }
    }


app = FastAPI()

# Configurar CORS para aceitar todas as origens
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cnx = pymysql.connect(
    user="root",
    password="YiQlVlvJsOFXPIYSDGTYTxndxArhwNSc",
    host="hopper.proxy.rlwy.net",
    database="railway",
    port=58780
)
cursor = cnx.cursor()


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

class CourseRequest(BaseModel):
    title: str
    description: str
    category: str
    level: str
    thumbnail: str
    price: str
    tags: List[str]
    published: bool

class ResourceSchema(BaseModel):
    title: str
    type: str
    url: str

class CodeExampleSchema(BaseModel):
    language: str
    code: str

class LessonSchema(BaseModel):
    title: str
    description: str
    content: str
    videoUrl: str
    duration: int
    order: int
    resources: List[ResourceSchema] = []
    codeExamples: List[CodeExampleSchema] = []

class ModuleRequest(BaseModel):
    title: str
    description: str
    order: int
    lessons: List[LessonSchema]

class UpdateProfileRequest(BaseModel):
    name: str
    bio: str
    avatar: str

@app.get("/")
async def main():
    return {"message": "Hello World"}




@app.post("/auth/login")
def login_user(login: LoginRequest):
    print(f"[LOGIN] Tentativa de login para: {login.email}")
    hashed_password = hashlib.sha256(login.password.encode('utf-8')).hexdigest()
    print(f"[LOGIN] Senha hash: {hashed_password}")
    query_select = f"SELECT id, nome, email, senha FROM users WHERE email = '{login.email}'"
    print(f"[LOGIN] Executando query: {query_select}")
    cursor.execute(query_select)
    user = cursor.fetchone()
    print(f"[LOGIN] Resultado do select: {user}")
    if not user:
        print("[LOGIN] Usuário não encontrado")
        return error_response("NOT_FOUND", "Usuário não encontrado", 404)
    user_id, name, email, db_password = user
    if db_password != hashed_password:
        print("[LOGIN] Senha incorreta")
        return error_response("UNAUTHORIZED", "Senha incorreta", 401)
    # Gerar JWT real
    token = jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(f"[LOGIN] Login bem-sucedido para {email} (id={user_id})")
    return success_response(
        "Login realizado com sucesso",
        {
            "user": {
                "id": f"usr_{user_id}",
                "name": name,
                "email": email,
                "bio": None,
                "avatar": None,
                "role": "user"
            },
            "token": token
        },
        200
    )
            



@app.post("/auth/register")
async def register_user(register: RegisterRequest):
    print(f"[REGISTER] Tentativa de registro para: {register.email}")
    # Verifica se o email já existe
    query_check = f"SELECT id FROM users WHERE email = '{register.email}'"
    print(f"[REGISTER] Executando query: {query_check}")
    cursor.execute(query_check)
    if cursor.fetchone():
        print("[REGISTER] Email já está em uso")
        return error_response(
            "VALIDATION_ERROR",
            "Dados inválidos",
            400,
            details=[{"field": "email", "message": "Email já está em uso"}]
        )
    senha_encr = hashlib.sha256(register.password.encode('utf-8')).hexdigest()
    print(f"[REGISTER] Senha hash: {senha_encr}")
    query_insert = f"""INSERT INTO `users` (`id`, `nome`, `email`, `senha`) VALUES (NULL, '{register.name}', '{register.email}', '{senha_encr}');"""
    print(f"[REGISTER] Executando query: {query_insert}")
    cursor.execute(query_insert)
    cnx.commit()
    user_id = cursor.lastrowid
    token = jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(f"[REGISTER] Registro bem-sucedido para {register.email} (id={user_id})")
    return success_response(
        "Usuário registrado com sucesso",
        {
            "user": {
                "id": f"usr_{user_id}",
                "name": register.name,
                "email": register.email,
                "bio": None,
                "avatar": None,
                "createdAt": "2024-01-15T10:30:00Z"
            },
            "token": token
        },
        201
    )


@app.post("/admin/courses")
def create_course(course: CourseRequest, Authorization: str = Header(...)):
    print(f"[CREATE COURSE] Payload: {course}")
    if not Authorization or not Authorization.startswith("Bearer "):
        print("[CREATE COURSE] Token inválido ou ausente")
        return error_response("UNAUTHORIZED", "Token inválido ou ausente", 401)
    query = f"""INSERT INTO courses (title, description, category, level, thumbnail, price, tags, published) VALUES ('{course.title}', '{course.description}', '{course.category}', '{course.level}', '{course.thumbnail}', '{course.price}', '{','.join(course.tags)}', {int(course.published)})"""
    print(f"[CREATE COURSE] Executando query: {query}")
    cursor.execute(query)
    cnx.commit()
    course_id = cursor.lastrowid
    print(f"[CREATE COURSE] Curso criado com id: {course_id}")
    return success_response(
        "Curso criado com sucesso",
        {
            "course": {
                "id": f"crs_{course_id}",
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "level": course.level,
                "thumbnail": course.thumbnail,
                "price": course.price,
                "tags": course.tags,
                "published": course.published,
                "createdAt": "2024-01-21T10:00:00Z",
                "totalModules": 0,
                "totalLessons": 0
            }
        },
        201
    )


@app.post("/admin/courses/{course_id}/modules")

def create_module(course_id: int, module: ModuleRequest, Authorization: str = Header(...)):
    print(f"[CREATE MODULE] Payload: {module}")
    if not Authorization or not Authorization.startswith("Bearer "):
        print("[CREATE MODULE] Token inválido ou ausente")
        return error_response("UNAUTHORIZED", "Token inválido ou ausente", 401)
    # Inserir módulo
    query_module = """
        INSERT INTO modules (courseId, title, description, `order`, totalLessons, totalDuration, createdAt)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    totalLessons = len(module.lessons)
    totalDuration = sum(lesson.duration for lesson in module.lessons)
    cursor.execute(query_module, (course_id, module.title, module.description, module.order, totalLessons, totalDuration))
    cnx.commit()
    module_id = cursor.lastrowid
    print(f"[CREATE MODULE] Módulo criado com id: {module_id}")
    lessons_response = []
    for idx, lesson in enumerate(module.lessons, start=1):
        # Inserir lição
        query_lesson = """
            INSERT INTO lessons (moduleId, title, description, content, videoUrl, duration, `order`, createdAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query_lesson, (module_id, lesson.title, lesson.description, lesson.content, lesson.videoUrl, lesson.duration, lesson.order))
        cnx.commit()
        lesson_id = cursor.lastrowid
        print(f"[CREATE LESSON] Lição: {lesson.title}, id: {lesson_id}")
        # Inserir recursos
        resources_response = []
        if hasattr(lesson, "resources") and lesson.resources:
            for resource in lesson.resources:
                query_resource = """
                    INSERT INTO resources (lessonId, title, type, url)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_resource, (lesson_id, resource.title, resource.type, resource.url))
                cnx.commit()
                resource_id = cursor.lastrowid
                print(f"[CREATE RESOURCE] Recurso: {resource.title}, id: {resource_id}")
                resources_response.append({
                    "id": resource_id,
                    "title": resource.title,
                    "type": resource.type,
                    "url": resource.url
                })
        lessons_response.append({
            "id": f"les_{lesson_id}",
            "title": lesson.title,
            "description": lesson.description,
            "duration": lesson.duration,
            "order": lesson.order,
            "resources": resources_response
        })
    return success_response(
        "Módulo criado com sucesso",
        {
            "module": {
                "id": f"mod_{module_id}",
                "courseId": f"crs_{course_id}",
                "title": module.title,
                "description": module.description,
                "order": module.order,
                "lessons": lessons_response,
                "totalLessons": len(lessons_response),
                "totalDuration": sum(l["duration"] for l in lessons_response),
                "createdAt": "2024-01-21T11:30:00Z"
            }
        },
        201
    )


# Exemplo de rota de perfil padronizada
@app.get("/profile/{user_id}")
def get_profile(user_id: int):
    query = f"SELECT id, nome, email, bio, avatar, createdAt, updatedAt FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    if not user:
        return error_response("NOT_FOUND", "Usuário não encontrado", 404)
    (
        id_, name, email, bio, avatar, created_at, updated_at
    ) = user
    # Buscar stats reais do usuário
    cursor.execute("SELECT COUNT(DISTINCT courseId) FROM user_progress WHERE userId = %s AND completed = 0", (user_id,))
    courses_in_progress = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT courseId) FROM user_progress WHERE userId = %s AND completed = 1", (user_id,))
    completed_courses = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE userId = %s AND completed = 1", (user_id,))
    total_lessons_watched = cursor.fetchone()[0]
    stats = {
        "coursesInProgress": courses_in_progress,
        "completedCourses": completed_courses,
        "totalLessonsWatched": total_lessons_watched
    }
    return success_response(
        "Perfil encontrado com sucesso",
        {
            "user": {
                "id": f"usr_{id_}",
                "name": name,
                "email": email,
                "bio": bio,
                "avatar": avatar,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "stats": stats
            }
        },
        200
    )

@app.put("/profile/{user_id}")
def update_profile(user_id: int, body: UpdateProfileRequest, Authorization: str = Header(...)):
    # Simulação de autenticação (em produção, validar token e user_id)
    if not Authorization or not Authorization.startswith("Bearer "):
        return error_response("UNAUTHORIZED", "Token inválido ou ausente", 401)
    # Atualizar usuário no banco
    query = f"UPDATE users SET nome = %s, bio = %s, avatar = %s, updatedAt = NOW() WHERE id = %s"
    cursor.execute(query, (body.name, body.bio, body.avatar, user_id))
    cnx.commit()
    # Buscar dados atualizados
    cursor.execute("SELECT id, nome, email, bio, avatar, updatedAt FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return error_response("NOT_FOUND", "Usuário não encontrado", 404)
    id_, name, email, bio, avatar, updated_at = user
    return success_response(
        "Perfil atualizado com sucesso",
        {
            "user": {
                "id": f"usr_{id_}",
                "name": name,
                "email": email,
                "bio": bio,
                "avatar": avatar,
                "updatedAt": updated_at
            }
        },
        200
    )


@app.get("/dashboard")
def get_dashboard(Authorization: str = Header(...)):
    if not Authorization or not Authorization.startswith("Bearer "):
        return error_response("UNAUTHORIZED", "Token inválido ou ausente", 401)
    token = Authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            return error_response("UNAUTHORIZED", "Token sem user_id", 401)
    except Exception as e:
        print(f"[DASHBOARD] Erro ao decodificar JWT: {e}")
        return error_response("UNAUTHORIZED", "Token inválido", 401)

    cursor.execute("SELECT nome, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return error_response("NOT_FOUND", "Usuário não encontrado", 404)
    name, email = user

    # Buscar progresso real do usuário
    cursor.execute("SELECT COUNT(DISTINCT courseId) FROM user_progress WHERE userId = %s AND completed = 0", (user_id,))
    courses_in_progress = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT courseId) FROM user_progress WHERE userId = %s AND completed = 1", (user_id,))
    completed_courses = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE userId = %s AND completed = 1", (user_id,))
    total_lessons_watched = cursor.fetchone()[0]

    progress = {
        "coursesInProgress": courses_in_progress,
        "completedCourses": completed_courses,
        "totalLessonsWatched": total_lessons_watched
    }

    cursor.execute("SELECT id, title, description FROM courses")
    courses = cursor.fetchall()
    courses_with_progress = []
    for row in courses:
        course_id = row[0]
        cursor.execute("SELECT COUNT(*) FROM modules WHERE courseId = %s", (course_id,))
        total_modules = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT moduleId) FROM user_progress WHERE userId = %s AND courseId = %s", (user_id, course_id))
        modules_completed = cursor.fetchone()[0]
        progress_percent = int((modules_completed / total_modules) * 100) if total_modules > 0 else 0
        courses_with_progress.append({
            "id": f"crs_{course_id}",
            "title": row[1],
            "description": row[2],
            "progress": progress_percent
        })

    return success_response(
        "Dashboard carregado com sucesso",
        {
            "user": {"name": name, "email": email},
            "progress": progress,
            "courses": courses_with_progress
        },
        200
    )

@app.get("/courses/categories")
def get_categories():
    cursor.execute("SELECT id, name, icon, description FROM categories")
    categories_db = cursor.fetchall()
    categories = []
    for row in categories_db:
        category_id, name, icon, description = row
        cursor.execute("SELECT COUNT(*) FROM courses WHERE category = %s", (category_id,))
        total_courses = cursor.fetchone()[0]
        categories.append({
            "id": category_id,
            "name": name,
            "icon": icon,
            "totalCourses": total_courses,
            "description": description
        })
    return success_response("Categorias carregadas com sucesso", {"categories": categories}, 200)

@app.get("/courses/{id}")
def get_course(id: int, Authorization: str = Header(...)):
    if not Authorization or not Authorization.startswith("Bearer "):
        return error_response("UNAUTHORIZED", "Token inválido ou ausente", 401)
    # Buscar curso
    cursor.execute("SELECT id, title, description FROM courses WHERE id = %s", (id,))
    course = cursor.fetchone()
    if not course:
        return error_response("NOT_FOUND", "Curso não encontrado", 404)
    course_id, title, description = course
    # Buscar módulos do curso
    cursor.execute("SELECT id, title, description FROM modules WHERE courseId = %s", (course_id,))
    modules_db = cursor.fetchall()
    modules = []
    # Buscar user_id do token
    user_id = None
    try:
        token = Authorization.split(" ", 1)[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
    except Exception:
        pass
    for module in modules_db:
        module_id, module_title, module_description = module
        # Buscar lições do módulo
        cursor.execute("SELECT id, title FROM lessons WHERE moduleId = %s", (module_id,))
        lessons_db = cursor.fetchall()
        lessons = []
        for lesson in lessons_db:
            lesson_id, lesson_title = lesson
            # Buscar progresso real da lição para o usuário
            completed = False
            if user_id:
                cursor.execute("SELECT completed FROM user_progress WHERE userId = %s AND lessonId = %s", (user_id, lesson_id))
                progress_row = cursor.fetchone()
                completed = bool(progress_row[0]) if progress_row else False
            lessons.append({
                "id": f"les_{lesson_id}",
                "title": lesson_title,
                "completed": completed
            })
        modules.append({
            "title": module_title,
            "description": module_description,
            "lessons": lessons
        })
    return success_response(
        "Curso carregado com sucesso",
        {
            "id": f"crs_{course_id}",
            "title": title,
            "description": description,
            "modules": modules
        },
        200
    )

@app.get("/lessons/{id}")
def get_lesson(id: int, Authorization: str = Header(None)):
    # Opcional: autenticação
    cursor.execute("SELECT id, moduleId, title, description, content, videoUrl, duration, `order`, createdAt FROM lessons WHERE id = %s", (id,))
    lesson = cursor.fetchone()
    if not lesson:
        return error_response("NOT_FOUND", "Lição não encontrada", 404)
    (
        lesson_id, module_id, title, description, content, video_url, duration, order, created_at
    ) = lesson
    # Buscar recursos da lição
    cursor.execute("SELECT id, title, type, url FROM resources WHERE lessonId = %s", (lesson_id,))
    resources_db = cursor.fetchall()
    resources = [
        {
            "id": resource[0],
            "title": resource[1],
            "type": resource[2],
            "url": resource[3]
        }
        for resource in resources_db
    ]
    return success_response(
        "Lição carregada com sucesso",
        {
            "id": f"les_{lesson_id}",
            "moduleId": module_id,
            "title": title,
            "description": description,
            "content": content,
            "videoUrl": video_url,
            "duration": duration,
            "order": order,
            "createdAt": created_at,
            "resources": resources
        },
        200
    )