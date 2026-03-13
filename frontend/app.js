const API_URL = "http://localhost:8000"; // ajuste para o endereço real da sua API

// --- Login ---
const loginSection = document.getElementById('login-section');
const adminSection = document.getElementById('admin-section');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');
const coursesList = document.getElementById('courses-list');
const showCreateCourseBtn = document.getElementById('show-create-course');
const createCourseFormDiv = document.getElementById('create-course-form');
const courseForm = document.getElementById('course-form');
const cancelCreateCourseBtn = document.getElementById('cancel-create-course');
const courseCreateError = document.getElementById('course-create-error');

function setToken(token) {
    localStorage.setItem('admin_token', token);
}
function getToken() {
    return localStorage.getItem('admin_token');
}
function clearToken() {
    localStorage.removeItem('admin_token');
}

function showLogin() {
    loginSection.style.display = '';
    adminSection.style.display = 'none';
}
function showAdmin() {
    loginSection.style.display = 'none';
    adminSection.style.display = '';
    loadCourses();
}

loginForm.onsubmit = async (e) => {
    e.preventDefault();
    loginError.textContent = '';
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (!data.success) throw new Error(data.error?.message || 'Erro ao logar');
        setToken(data.data.token);
        showAdmin();
    } catch (err) {
        loginError.textContent = err.message;
    }
};

logoutBtn.onclick = () => {
    clearToken();
    showLogin();
};

function courseItemHtml(course, idx) {
    return `<div class="course-item" data-idx="${idx}">
        <strong>${course.title}</strong><br>
        <span>${course.description}</span><br>
        <span>Categoria: ${course.category || ''} | Nível: ${course.level || ''}</span>
    </div>`;
}

// --- Gerenciamento de Módulos, Lições e Recursos ---
function moduleItemHtml(module, courseId) {
    return `<div class="module-item">
        <strong>${module.title}</strong> <button onclick="showCreateLesson(${courseId},${module.id})">+ Lição</button><br>
        <span>${module.description}</span>
        <div class="lessons-list" id="lessons-list-${module.id}"></div>
    </div>`;
}

function lessonItemHtml(lesson) {
    return `<div class="lesson-item">
        <strong>${lesson.title}</strong><br>
        <span>${lesson.description || ''}</span>
    </div>`;
}

async function loadModules(courseId) {
    const modulesDiv = document.createElement('div');
    modulesDiv.innerHTML = 'Carregando módulos...';
    try {
        const res = await fetch(`${API_URL}/courses/${courseId}`, {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        const data = await res.json();
        if (!data.success) throw new Error(data.error?.message || 'Erro ao buscar módulos');
        modulesDiv.innerHTML = '';
        data.data.modules.forEach((module, idx) => {
            modulesDiv.innerHTML += moduleItemHtml(module, courseId);
            // Carregar lições do módulo
            setTimeout(() => loadLessons(module, modulesDiv.querySelector(`#lessons-list-${module.id}`)), 0);
        });
    } catch (err) {
        modulesDiv.innerHTML = `<div class="error">${err.message}</div>`;
    }
    return modulesDiv;
}

async function loadLessons(module, lessonsDiv) {
    lessonsDiv.innerHTML = '';
    module.lessons.forEach(lesson => {
        lessonsDiv.innerHTML += lessonItemHtml(lesson);
    });
}

// Exibir módulos ao clicar em um curso
coursesList.onclick = async (e) => {
    const courseItem = e.target.closest('.course-item');
    if (!courseItem) return;
    const idx = courseItem.getAttribute('data-idx');
    const courseId = window.lastCourses[idx]?.id?.replace('crs_', '');
    if (!courseId) return;
    // Evitar múltiplas aberturas
    if (courseItem.querySelector('.modules-div')) return;
    const modulesDiv = await loadModules(courseId);
    modulesDiv.classList.add('modules-div');
    courseItem.appendChild(modulesDiv);
};

// Salvar referência dos cursos carregados
window.lastCourses = [];
async function loadCourses() {
    coursesList.innerHTML = 'Carregando...';
    try {
        const res = await fetch(`${API_URL}/dashboard`, {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        const data = await res.json();
        if (!data.success) throw new Error(data.error?.message || 'Erro ao buscar cursos');
        coursesList.innerHTML = '';
        window.lastCourses = data.data.courses;
        data.data.courses.forEach((course, idx) => {
            coursesList.innerHTML += courseItemHtml(course, idx);
        });
    } catch (err) {
        coursesList.innerHTML = `<div class="error">${err.message}</div>`;
    }
}

showCreateCourseBtn.onclick = () => {
    createCourseFormDiv.style.display = '';
};
cancelCreateCourseBtn.onclick = () => {
    createCourseFormDiv.style.display = 'none';
    courseCreateError.textContent = '';
    courseForm.reset();
};

courseForm.onsubmit = async (e) => {
    e.preventDefault();
    courseCreateError.textContent = '';
    const payload = {
        title: document.getElementById('course-title').value,
        description: document.getElementById('course-description').value,
        category: document.getElementById('course-category').value,
        level: document.getElementById('course-level').value,
        thumbnail: document.getElementById('course-thumbnail').value,
        price: document.getElementById('course-price').value,
        tags: document.getElementById('course-tags').value.split(',').map(t => t.trim()).filter(Boolean),
        published: document.getElementById('course-published').checked
    };
    try {
        const res = await fetch(`${API_URL}/admin/courses`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getToken()
            },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!data.success) throw new Error(data.error?.message || 'Erro ao criar curso');
        createCourseFormDiv.style.display = 'none';
        courseForm.reset();
        loadCourses();
    } catch (err) {
        courseCreateError.textContent = err.message;
    }
};

// Inicialização
if (getToken()) {
    showAdmin();
} else {
    showLogin();
}
