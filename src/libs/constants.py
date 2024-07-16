DEFAULT_CONFIG_FILE = ".docpose.yml"
DEFAULT_CONFIG_SAMPLE_FILE = ".docpose-sample.yml"
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
'README: https://github.com/ehildt/docpose'
)

SAMPLE_CONFIG = (
'''
backend: &BACKEND backend.j2    # using yaml anchors to omit value redundancy and hardcoding
kafka: &KAFKA kafka.j2
webui: &WEBUI web-ui.j2
keydb: &KEYDB keydb.j2
mongo: &MONGO mongo.j2
minio: &MINIO minio.j2

default_output: &DEFAULT_OUTPUT compose.yml
webui_output: &WEBUI_OUTPUT web-ui.yml

source:
  template_dir: .templates
  outputs:
    - *DEFAULT_OUTPUT
    - *WEBUI_OUTPUT
  env_files:
    - .env
    - .env.local
  environment:
    - NODE_ENV: local
    - TARGET: local

compose:
  - service.j2

  - template: *BACKEND
    environment:
      - TARGET: production
    output: *DEFAULT_OUTPUT
    depends_on:
      - *KAFKA
      - *KEYDB
      - *MONGO
      - *MINIO

  - template: *KEYDB
    output: *DEFAULT_OUTPUT
    depends_on:
      - *BACKEND

  - template: *MONGO
    output: *DEFAULT_OUTPUT
    depends_on:
      - *BACKEND

  - template: *MINIO
    output: *DEFAULT_OUTPUT
    depends_on:
      - *BACKEND

  - template: *WEBUI
    output: *WEBUI_OUTPUT
    depends_on:
      - *BACKEND

  - template: *KAFKA
    output: *DEFAULT_OUTPUT
    environment:
      - PASSWORD: $PASSWORD
        toEqual: 1234
      - USERNAME: $USERNAME
        toEqual: admin

  - template: kafdrop.j2
    depends_on:
      - *KAFKA
    output: *DEFAULT_OUTPUT
    
  - template: volumes.j2
    output: *DEFAULT_OUTPUT

  - template: networks.j2
    output: *DEFAULT_OUTPUT
'''
)