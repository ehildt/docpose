DEFAULT_CONFIG_FILE = ".docpose.yml"
DEFAULT_LOCAL_ENV_FILE = ".env.local"

TO_CONTAIN = 'toContain'
TO_EQUAL = 'toEqual'
TO_BE_LOE = 'toBeLoE'
TO_BE_GOE = 'toBeGoE'


DESCRIPTION = (
'Docpose is a tool designed for generating and managing configuration files.\n' 
'The name combines "doc" (from Docker) and "pose" (from Compose).\n' 
'Its capabilities include:\n\n'
' - Template Processing:\n' 
'   Utilizes Jinja2, a powerful templating engine for Python, to process templates.\n\n'
' - Environment Variables:\n' 
'   Environment variables specified in the configuration file are injected into every template,\n' 
'   enabling dynamic and customizable configurations.\n\n'
'Docpose is not limited to Docker Compose but can be used with any type of configuration file,\n'
'making it a flexible solution for various use cases'
)

SAMPLE_CONFIG = (
'''
source:
  template_dir: .templates
  outputs:
    - compose.yml
    - &WEB_UI web_ui.yml
  env_files:
    - some_path_to/env/.env
    - another_path_to/env/.env.local
  environment:
    - NODE_ENV: local
    - TARGET: local

compose:
  - template: &BACKEND backend.j2
    depends_on:
      - *KAFKA
  - template: web-ui.j2
    depends_on:
      - *BACKEND
  - template: &KAFKA kafka.j2
    depends_on:
      - *BACKEND
    environment:
      - PASSWORD: $PASSWORD
        toEqual: 1234
      - USERNAME: $USERNAME
        toEqual: admin
  - template: kafdrop.j2
    depends_on:
      - *KAFKA
    output: *WEB_UI
  - volumes.j2
  - networks.j2

command: docker compose
'''
)