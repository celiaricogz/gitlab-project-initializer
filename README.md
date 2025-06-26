# 🛠️ GitLab Project Initializer

**GitLab Project Initializer** es una herramienta que automatiza la inicialización de nuevos repositorios en GitLab CE (Community Edition) sin suscripción. Está diseñada para cubrir limitaciones de la versión gratuita y facilitar la puesta en marcha de proyectos nuevos, aplicando una estructura base y protecciones desde una plantilla predefinida.

> 🔧 Proyecto en uso real en entorno corporativo cerrado, ejecutado contra un servidor GitLab autoalojado, sin funcionalidades premium.

---

## 🚀 ¿Qué hace esta herramienta?

- Detecta nuevos proyectos creados recientemente en GitLab
- Clona un repositorio plantilla (estructura base)
- Inicializa el nuevo repositorio con el contenido de la plantilla
- Crea y sube ramas `main` y `develop`
- Protege automáticamente las ramas (`push/merge` solo para mantenedores)
- Puede ejecutarse manualmente o como un servicio `systemd` programado

---

## 📁 Estructura del proyecto

```
.
├── gitlab-project-initializer.py       # Script principal
├── gitlan-project-initilizer.service   # Unidad de systemd para ejecutar el script como servicio
├── gitlab-project-initilizer.timer     # Timer de systemd para ejecución periódica
```

---

## ⚙️ Requisitos

- Python 3
- Dependencias:
  - `requests`
  - `gitpython`
- Acceso SSH a GitLab (servidor local o remoto)
- Token de API de GitLab con permisos de acceso a proyectos

---

## 🔧 Configuración

Edita las siguientes variables al inicio del script:

```python
GITLAB_URL = "https://gitlab.tuempresa.local"
PRIVATE_TOKEN = "TU_TOKEN"
TEMPLATE_REPO_SSH = "git@...:template/repo.git"
CHECK_INTERVAL_MINUTES = 5  # Intervalo de búsqueda de nuevos proyectos
```

---

## 🧪 Cómo se usa manualmente

1. Asegúrate de tener Python 3 y las dependencias instaladas:

```bash
pip install requests gitpython
```

2. Ejecuta el script:

```bash
python3 gitlab-project-initializer.py
```

---

## 🛠️ Uso como servicio con systemd

Este proyecto incluye archivos de unidad y temporizador `systemd` para ejecutar el script automáticamente cada 2 minutos.

### Archivos incluidos:

- `gitlan-project-initilizer.service`: define el servicio
- `gitlab-project-initilizer.timer`: define la frecuencia de ejecución

### Instalación:

```bash
sudo cp gitlan-project-initilizer.service /etc/systemd/system/
sudo cp gitlab-project-initilizer.timer /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable gitlab-project-initilizer.timer
sudo systemctl start gitlab-project-initilizer.timer
```

Este setup ejecutará el script automáticamente cada 2 minutos tras el arranque del sistema.

---

## 🧠 ¿Para qué es útil?

- Automatizar la inicialización de proyectos en GitLab sin suscripción
- Asegurar que todos los repos comienzan con la misma estructura y configuración
- Aplicar buenas prácticas de versionado (ramas protegidas, control de flujos)
- Reducir errores y carga manual en la gestión de nuevos proyectos

---

## 🛡️ Limitaciones y posibles mejoras

- Solo inicializa repos vacíos creados recientemente
- No gestiona CI/CD ni configuración adicional (por ahora)
- No aplica configuración diferenciada por tipo de proyecto (genérico)
- Mejorable para entornos más complejos o segmentados

---

## 🧩 Próximas mejoras previstas

- [ ] Soporte para plantillas distintas según tipo de proyecto
- [ ] Integración con GitLab CI para aplicar configuraciones base
- [ ] Registro de acciones e histórico en log
- [ ] Configuración vía archivo externo (.env o JSON)

---

## 👩‍💻 Autora

**Celia Rico Gutiérrez**  
Ingeniera DevOps & Fullstack — Automatización de entornos, sistemas Linux y control de versiones.  
🔗 [LinkedIn](https://www.linkedin.com/in/celiaricogutierrez)  
🔗 [Perfil en Malt](https://www.malt.es/profile/celiaricogutierrez)

---

📅 _Última actualización: Junio 2025_
