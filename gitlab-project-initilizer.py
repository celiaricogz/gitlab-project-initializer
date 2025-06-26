import os
import requests
import shutil
import logging
from datetime import datetime, timedelta
import git

# CONFIGURACIÓN
GITLAB_URL = "YOUR URL"
PRIVATE_TOKEN = "YOUR TOKEN"
TEMPLATE_REPO_SSH = "YOUR TEMPLATE"
CHECK_INTERVAL_MINUTES = 5

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cabecera para la API
headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

def get_recent_projects():
    since = (datetime.utcnow() - timedelta(minutes=CHECK_INTERVAL_MINUTES)).isoformat()
    url = f"{GITLAB_URL}/api/v4/projects?created_after={since}&order_by=created_at&sort=desc&simple=true&per_page=50"
    response = requests.get(url, headers=headers)
    return response.json()

def is_repository_empty(project_id):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/tree"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        return len(content) == 0
    elif response.status_code == 404:
        # Posible que aún no se haya inicializado
        return True
    else:
        logging.warning(f"No se pudo verificar si el proyecto {project_id} está vacío. Código: {response.status_code}")
        return False

def protect_branch(project_id, branch_name, retries=5, delay=2):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/protected_branches"
    data = {
        "name": branch_name,
        "push_access_level": 40,
        "merge_access_level": 40,
        "unprotect_access_level": 40
    }

    for attempt in range(retries):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            logging.info(f"Rama '{branch_name}' protegida correctamente.")
            return
        elif response.status_code == 409:
            logging.info(f"La rama '{branch_name}' ya estaba protegida.")
            return
        elif response.status_code == 400 and "Branch 'develop' does not exist" in response.text:
            logging.warning(f"La rama '{branch_name}' aún no está disponible. Reintentando en {delay} segundos...")
            time.sleep(delay)
        else:
            logging.error(f"Error al proteger la rama '{branch_name}': {response.status_code} - {response.text}")
            break

def initialize_project(project):
    project_name = project['name']
    ssh_url = project['ssh_url_to_repo']
    temp_dir = f"/tmp/{project_name}"

    logging.info(f"Iniciando proyecto {project_name}...")

    if not is_repository_empty(project['id']):
        logging.info(f"El proyecto {project_name} ya tiene contenido y no será sobrescrito.")
        return

    os.makedirs(temp_dir, exist_ok=True)
    try:
        # Clonar la plantilla
        repo = git.Repo.clone_from(TEMPLATE_REPO_SSH, temp_dir)

        # Configurar usuario
        with repo.config_writer() as cw:
            cw.set_value("user", "name", "InitBot")
            cw.set_value("user", "email", "initbot@gitlab.local")

        # Reescribir remote y hacer push
        origin = repo.remote("origin")
        origin.set_url(ssh_url)
        repo.git.push('--force', 'origin', '--all')
        repo.git.push('--force', 'origin', '--tags')

        # Crear rama develop a partir de main
        repo.git.checkout('-b', 'develop')
        repo.git.push('--set-upstream', 'origin', 'develop')

        # Proteger la rama develop
        protect_branch(project['id'], 'develop')


        logging.info(f"Proyecto {project_name} inicializado exitosamente.")
    except Exception as e:
        logging.error(f"Error al inicializar el proyecto {project_name}: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def main():
    projects = get_recent_projects()
    if not projects:
        print("No se encontraron proyectos nuevos.")
        return
    for project in projects:
        initialize_project(project)

if __name__ == "__main__":
    main()
