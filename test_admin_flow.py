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
        "name": "Admin JavaScript",
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

def create_js_course(token):
    url = f"{BASE_URL}/admin/courses"
    
    # Configuração do curso de JavaScript
    category = "javascript"
    level = "beginner"  # Pode ser: beginner, intermediate, advanced
    
    course_data = {
        "title": "JavaScript Completo: Do Básico ao Avançado",
        "description": "Aprenda JavaScript do zero e se torne um desenvolvedor full-stack. Curso completo com mais de 50 aulas práticas, projetos reais e exercícios.",
        "category": category,
        "level": level,
        "thumbnail": "https://cdn.suaplataforma.com/cursos/javascript-completo.jpg",
        "price": "free",
        "tags": ["javascript", "frontend", "backend", "web", "programação", "js", "ecmascript"],
        "published": True
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=course_data, headers=headers)
    print("[CREATE JS COURSE] Status:", response.status_code)
    print("[CREATE JS COURSE] Response:", response.json())
    
    course_id = response.json().get("data", {}).get("course", {}).get("id")
    if course_id and isinstance(course_id, str) and course_id.startswith("crs_"):
        course_id = int(course_id.replace("crs_", ""))
    
    return course_id

def create_js_modules(token, course_id):
    url = f"{BASE_URL}/admin/courses/{course_id}/modules"
    
    # Módulos completos de JavaScript
    modules = [
        # Módulo 1: Introdução e Fundamentos
        {
            "title": "Módulo 1: Introdução ao JavaScript",
            "description": "Conheça a história do JavaScript, configuração do ambiente e primeiros passos com a linguagem.",
            "order": 1,
            "lessons": [
                {
                    "title": "O que é JavaScript? História e Evolução",
                    "description": "Conheça a história do JavaScript, sua criação e evolução até os dias atuais.",
                    "content": "JavaScript foi criado em 1995 por Brendan Eich enquanto trabalhava na Netscape. Inicialmente chamado de Mocha, depois LiveScript e finalmente JavaScript. Hoje é uma das linguagens mais populares do mundo, rodando tanto no frontend quanto no backend.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/intro-js.mp4",
                    "duration": 480,  # 8 minutos
                    "order": 1,
                    "resources": [
                        {
                            "title": "Slide da Aula - Introdução ao JS",
                            "type": "pdf",
                            "url": "https://cdn.suaplataforma.com/resources/js/intro-slides.pdf"
                        }
                    ]
                },
                {
                    "title": "Configurando o Ambiente de Desenvolvimento",
                    "description": "Instale e configure as ferramentas necessárias para programar em JavaScript.",
                    "content": "Vamos instalar o VS Code, Node.js e configurar o ambiente de desenvolvimento. Aprenda a usar o console do navegador e os primeiros comandos.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/setup.mp4",
                    "duration": 600,  # 10 minutos
                    "order": 2,
                    "resources": [
                        {
                            "title": "Guia de Instalação",
                            "type": "pdf",
                            "url": "https://cdn.suaplataforma.com/resources/js/guia-instalacao.pdf"
                        }
                    ]
                },
                {
                    "title": "Primeiro Programa: Hello World",
                    "description": "Crie seu primeiro programa em JavaScript e entenda a sintaxe básica.",
                    "content": "Vamos criar nosso primeiro programa 'Hello World' usando diferentes métodos: console.log, alert e document.write. Entenda a estrutura básica de um programa JavaScript.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/hello-world.mp4",
                    "duration": 360,  # 6 minutos
                    "order": 3
                }
            ]
        },
        
        # Módulo 2: Variáveis e Tipos de Dados
        {
            "title": "Módulo 2: Variáveis e Tipos de Dados",
            "description": "Aprenda a trabalhar com variáveis e os diferentes tipos de dados em JavaScript.",
            "order": 2,
            "lessons": [
                {
                    "title": "Variáveis: var, let e const",
                    "description": "Entenda as diferenças entre var, let e const e quando usar cada uma.",
                    "content": "As variáveis em JavaScript evoluíram com o ECMAScript 6. Aprenda sobre escopo, hoisting e as diferenças cruciais entre var, let e const para escrever código mais seguro.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/variaveis.mp4",
                    "duration": 540,  # 9 minutos
                    "order": 1,
                    "resources": [
                        {
                            "title": "Tabela Comparativa - var, let, const",
                            "type": "pdf",
                            "url": "https://cdn.suaplataforma.com/resources/js/comparativo-varletconst.pdf"
                        }
                    ]
                },
                {
                    "title": "Tipos Primitivos: String, Number, Boolean",
                    "description": "Trabalhe com os tipos primitivos fundamentais do JavaScript.",
                    "content": "Explore os tipos primitivos: strings (texto), numbers (números inteiros e decimais), booleans (true/false), null e undefined. Aprenda a converter entre tipos.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/tipos-primitivos.mp4",
                    "duration": 600,  # 10 minutos
                    "order": 2
                },
                {
                    "title": "Operadores Aritméticos e Lógicos",
                    "description": "Utilize operadores para realizar cálculos e comparações.",
                    "content": "Aprenda a usar operadores aritméticos (+, -, *, /, %), operadores de comparação (==, ===, !=, !==, >, <) e operadores lógicos (&&, ||, !).",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/operadores.mp4",
                    "duration": 540,  # 9 minutos
                    "order": 3
                }
            ]
        },
        
        # Módulo 3: Estruturas de Controle
        {
            "title": "Módulo 3: Estruturas de Controle",
            "description": "Controle o fluxo do seu programa com condicionais e loops.",
            "order": 3,
            "lessons": [
                {
                    "title": "Condicionais: if, else if, else",
                    "description": "Tome decisões no seu código com estruturas condicionais.",
                    "content": "Aprenda a usar if, else if e else para criar lógica condicional. Entenda a importância das chaves e boas práticas.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/condicionais.mp4",
                    "duration": 540,
                    "order": 1
                },
                {
                    "title": "Switch Statement",
                    "description": "Simplifique múltiplas condições com o switch.",
                    "content": "O switch é uma alternativa elegante para múltiplos if-else. Aprenda sua sintaxe, o uso do break e casos especiais.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/switch.mp4",
                    "duration": 420,
                    "order": 2
                },
                {
                    "title": "Loops: for, while, do while",
                    "description": "Repita blocos de código com diferentes tipos de loops.",
                    "content": "Domine os loops em JavaScript: for (para contagens), while (para condições) e do-while (executa pelo menos uma vez).",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/loops.mp4",
                    "duration": 660,
                    "order": 3,
                    "resources": [
                        {
                            "title": "Exercícios de Loops",
                            "type": "pdf",
                            "url": "https://cdn.suaplataforma.com/resources/js/exercicios-loops.pdf"
                        }
                    ]
                }
            ]
        },
        
        # Módulo 4: Funções
        {
            "title": "Módulo 4: Funções - O Coração do JavaScript",
            "description": "Aprenda a criar e utilizar funções, um dos conceitos mais importantes da linguagem.",
            "order": 4,
            "lessons": [
                {
                    "title": "Declaração de Funções e Parâmetros",
                    "description": "Crie suas primeiras funções e entenda parâmetros.",
                    "content": "Funções são blocos de código reutilizáveis. Aprenda a declarar funções, passar parâmetros e retornar valores.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/funcoes-basico.mp4",
                    "duration": 600,
                    "order": 1
                },
                {
                    "title": "Function Expression e Arrow Functions",
                    "description": "Explore diferentes formas de criar funções em JavaScript.",
                    "content": "Além da declaração tradicional, JavaScript oferece function expressions e arrow functions (ES6). Entenda as diferenças e quando usar cada uma.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/arrow-functions.mp4",
                    "duration": 540,
                    "order": 2
                },
                {
                    "title": "Escopo e Closures",
                    "description": "Entenda como o escopo funciona e o poderoso conceito de closures.",
                    "content": "Escopo determina onde variáveis são acessíveis. Closures são funções que 'lembram' do ambiente onde foram criadas - um conceito avançado mas essencial.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/closures.mp4",
                    "duration": 720,
                    "order": 3
                }
            ]
        },
        
        # Módulo 5: Arrays e Objetos
        {
            "title": "Módulo 5: Arrays e Objetos",
            "description": "Trabalhe com estruturas de dados fundamentais em JavaScript.",
            "order": 5,
            "lessons": [
                {
                    "title": "Arrays: Métodos Básicos",
                    "description": "Crie e manipule arrays com métodos essenciais.",
                    "content": "Arrays são listas ordenadas. Aprenda a criar, acessar e modificar arrays usando push, pop, shift, unshift, splice e mais.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/arrays-basico.mp4",
                    "duration": 600,
                    "order": 1
                },
                {
                    "title": "Métodos de Iteração: forEach, map, filter",
                    "description": "Domine os métodos modernos para trabalhar com arrays.",
                    "content": "forEach para iterar, map para transformar, filter para filtrar. Esses métodos tornam seu código mais limpo e funcional.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/array-methods.mp4",
                    "duration": 720,
                    "order": 2,
                    "resources": [
                        {
                            "title": "Cheat Sheet - Métodos de Array",
                            "type": "pdf",
                            "url": "https://cdn.suaplataforma.com/resources/js/cheatsheet-arrays.pdf"
                        }
                    ]
                },
                {
                    "title": "Objetos: Propriedades e Métodos",
                    "description": "Trabalhe com objetos, a base para dados estruturados.",
                    "content": "Objetos em JavaScript são coleções de pares chave-valor. Aprenda a criar, acessar e manipular objetos, além de métodos úteis como Object.keys, Object.values.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/objetos.mp4",
                    "duration": 600,
                    "order": 3
                }
            ]
        },
        
        # Módulo 6: DOM - Manipulação de Páginas Web
        {
            "title": "Módulo 6: Manipulação do DOM",
            "description": "Aprenda a interagir com elementos HTML e criar páginas dinâmicas.",
            "order": 6,
            "lessons": [
                {
                    "title": "Selecionando Elementos",
                    "description": "Aprenda a selecionar elementos HTML com JavaScript.",
                    "content": "Use métodos como getElementById, querySelector, querySelectorAll para encontrar elementos na página e prepará-los para manipulação.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/dom-seletores.mp4",
                    "duration": 540,
                    "order": 1
                },
                {
                    "title": "Manipulando Conteúdo e Atributos",
                    "description": "Altere textos, HTML e atributos dos elementos.",
                    "content": "Modifique o conteúdo com textContent e innerHTML. Altere atributos como src, href, class usando setAttribute e propriedades diretas.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/dom-manipulacao.mp4",
                    "duration": 600,
                    "order": 2
                },
                {
                    "title": "Eventos: Respondendo a Ações do Usuário",
                    "description": "Torne suas páginas interativas com eventos.",
                    "content": "Aprenda a responder a cliques, movimentos de mouse, teclas e outros eventos. Use addEventListener e entenda o objeto de evento.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/eventos.mp4",
                    "duration": 720,
                    "order": 3
                }
            ]
        },
        
        # Módulo 7: JavaScript Moderno (ES6+)
        {
            "title": "Módulo 7: JavaScript Moderno (ES6+)",
            "description": "Explore as funcionalidades modernas do JavaScript.",
            "order": 7,
            "lessons": [
                {
                    "title": "Template Strings e Destructuring",
                    "description": "Trabalhe com strings de forma mais elegante e desestruturação.",
                    "content": "Template strings permitem interpolação e strings multilinha. Destructuring facilita extrair valores de arrays e objetos.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/template-destructuring.mp4",
                    "duration": 540,
                    "order": 1
                },
                {
                    "title": "Spread Operator e Rest Parameters",
                    "description": "Use ... para espalhar e agrupar elementos.",
                    "content": "O spread operator expande elementos. Rest parameters agrupam argumentos em um array. Funcionalidades poderosas para manipular coleções.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/spread-rest.mp4",
                    "duration": 480,
                    "order": 2
                },
                {
                    "title": "Promises e Async/Await",
                    "description": "Trabalhe com operações assíncronas de forma elegante.",
                    "content": "Promises representam valores futuros. Async/await é açúcar sintático para trabalhar com promises de forma mais legível. Essencial para chamadas de API.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/async-await.mp4",
                    "duration": 780,
                    "order": 3,
                    "resources": [
                        {
                            "title": "Guia de Async/Await",
                            "type": "pdf",
                            "url": "https://cdn.suaplataforma.com/resources/js/guia-async-await.pdf"
                        }
                    ]
                }
            ]
        },
        
        # Módulo 8: Projeto Prático - Lista de Tarefas
        {
            "title": "Módulo 8: Projeto Prático - Lista de Tarefas",
            "description": "Aplique tudo que aprendeu criando um projeto completo.",
            "order": 8,
            "lessons": [
                {
                    "title": "Estruturando o Projeto",
                    "description": "Planeje e estruture seu aplicativo de lista de tarefas.",
                    "content": "Vamos planejar nosso projeto Todo List: funcionalidades, estrutura de arquivos (HTML, CSS, JS) e organização do código.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/projeto-estrutura.mp4",
                    "duration": 600,
                    "order": 1
                },
                {
                    "title": "Implementando a Interface",
                    "description": "Crie a interface HTML e CSS do projeto.",
                    "content": "Desenvolva a interface do usuário: formulário para adicionar tarefas, lista para exibir, botões para marcar como concluído e excluir.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/projeto-interface.mp4",
                    "duration": 720,
                    "order": 2
                },
                {
                    "title": "Funcionalidades com JavaScript",
                    "description": "Adicione interatividade ao projeto.",
                    "content": "Implemente as funcionalidades: adicionar tarefa, marcar como concluída, excluir, filtrar (todas, ativas, concluídas) e salvar no localStorage.",
                    "videoUrl": "https://cdn.suaplataforma.com/videos/js/projeto-logica.mp4",
                    "duration": 900,
                    "order": 3,
                    "resources": [
                        {
                            "title": "Código Fonte do Projeto",
                            "type": "code",
                            "url": "https://github.com/suaplataforma/js-todo-list"
                        }
                    ]
                }
            ]
        }
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n=== CRIANDO MÓDULOS DO CURSO DE JAVASCRIPT ===\n")
    
    for module_data in modules:
        print(f"Criando: {module_data['title']}")
        print(f"  Lições: {len(module_data['lessons'])}")
        
        response = requests.post(url, json=module_data, headers=headers)
        
        if response.status_code == 201:
            print(f"  ✅ Status: {response.status_code} - Sucesso!")
        else:
            print(f"  ❌ Status: {response.status_code}")
            print(f"  Resposta: {response.json()}")
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 INICIANDO CRIAÇÃO DO CURSO COMPLETO DE JAVASCRIPT\n")
    
    # Registrar admin
    email, password, token = register_admin()
    if not token:
        print("📝 Realizando login...")
        token = login_admin(email, password)
    
    if token:
        print("\n📚 Criando curso de JavaScript...")
        course_id = create_js_course(token)
        
        if course_id:
            print(f"✅ Curso criado com sucesso! ID: {course_id}")
            
            # Criar todos os módulos
            create_js_modules(token, course_id)
            
            print("\n" + "="*50)
            print("🎉 CURSO DE JAVASCRIPT CRIADO COM SUCESSO!")
            print(f"📊 Total: 8 módulos com mais de 30 lições")
            print("="*50)
        else:
            print("❌ Falha ao criar curso")