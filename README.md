# DOCPOSE

![Version](https://img.shields.io/badge/docpose-1.2.1-blue)
![Python 3](https://img.shields.io/badge/python-3-blue.svg)
![Jinja2](https://img.shields.io/badge/jinja2-2.11.3-green.svg)
![Open Source](https://badgen.net/badge/Open%20Source/❤/red)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)

A small and simple templating engine build on top of python and jinja2.

## COMMANDS

`docpose -v` shows the version number.

`docpose -i` generates a .docpose-sample.yml.

`docpose -c .docpose.yml` generates the *compose.yml*

## KICKOFF

- Install docpose `pip3 install docpose`
- Generate a sample **.docpose-sample.yml** `docpose -i`
- Edit the **.docpose-sample.yml** and if necessary rename it aka .docpose.yml
- Generate the **compose.yml** with `docpose -c .docpose.yml (the renamed sample file)`

### The Config YML Explained

Create **constants** so that you can reuse them across the yml file (anchors):

```yml
backend: &BACKEND backend.j2
kafka: &KAFKA kafka.j2
webui: &WEBUI web-ui.j2
keydb: &KEYDB keydb.j2
mongo: &MONGO mongo.j2
minio: &MINIO minio.j2

default_output: &DEFAULT_OUTPUT compose.yml
webui_output: &WEBUI_OUTPUT web-ui.yml
```

Define the source which tells docpose where to find the templates etc.

```yml
source:
  template_dir: .templates  # path to templates

  outputs:                  # can be a string or a list of strings
    - *DEFAULT_OUTPUT       # use either a constant which we defined as an anchor
    - *WEBUI_OUTPUT         # or, if you don't like yml anchors, use the value directly (web-ui.yml)

  env_files:                # a list of .env files which are used as a default
    - .env                  # except for the .env.local other .env files need to exist
    - .env.local            # this file is always optional, overwrites vars coming from the other files

  environment:              # an alternative way to set system variables. these overwrite those in env_files 
    - NODE_ENV: local       # NODE_ENV will overwrite the system variable (NODE_ENV) coming from env_files
    - TARGET: local         # TARGET will overwrite the system variable (TARGET) coming from env_files
```

Before we move on, let's talk about the optional template context.

```yml
compose: 
    - service.j2                # a template can be a simple string
                                # in this case the template has access 
                                # to all the system environment variables which 
                                # are set in the source

    - template: service.j2      # a template can also have it's own "context"

      environment:              # (optional) overwrites the system environment variables
        - TARGET: <value>       # overwrites TARGET for this particular template
          toBeGoE: <number>     # checks if TARGET is greater or equal to <number>
          toBeLoE: <number>     # checks if TARGET is less or equal to <number>
          toContain: <string>   # checks if <string> is a substring in TARGET
          toEqual: <value>      # will check TARGET for strict equality.
                                # supported types: [string|int|float|boolean|$SYSTEM_VARS] 

      output: *DEFAULT_OUTPUT   # if source::outputs is a list, then output is mandatory
                                # the output needs to be one of the 
                                # values which are declared in source::outputs 

      depends_on:               # (optional) the depends_on checks the dependency on another template
            - *KAFKA            # checks, if the kafka template is part of the composition
            - *KEYDB            # if the dependency is not fulfilled, an error is thrown
            - $ENV_VAR          # checks if $ENV_VAR resolves to true; skips the template otherwise  
                                # $ENV_VAR is falsy if it's an empty string, 0, false
```

Here is a full example of how a template composition could look like:

```yml
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
      - $USE_KAFKA
    output: *DEFAULT_OUTPUT
    
  - template: volumes.j2
    output: *DEFAULT_OUTPUT

  - template: networks.j2
    output: *DEFAULT_OUTPUT
```

## How Does A Template Look Like

A template follows the syntax of the popular python library [jinja2](https://palletsprojects.com/p/jinja/).

```j2
  backend:
    container_name: backend
    build:
      context: ./apps/backend
      target: local
    volumes:
      - ./apps/backend:/app
      - ./node_modules:/node_modules
    depends_on:
    {%- if USE_MONGODB %}
      - mongo
    {%- endif %} 
    {%- if USE_MINIO %}
      - minio
    {%- endif %} 
    {%- if USE_KEYDB %}
      - keydb
    {%- endif %} 
    {%- if USE_KAFKA or USE_MQTT or USE_RABBITMQ %}
      - msbridge
    {%- endif %} 
    env_file:
      - ./apps/backend/env/.env
    environment:
      - NODE_ENV={{ TARGET }}
      - PRINT_ENV=false
    ports:
      - 3001:3001
    networks:
      - acap-network
```

## What ChatGPT Has To Say

### Simplicity and Elegance of Docpose

Docpose offers a streamlined and intuitive approach for managing templated configurations, focusing on simplicity and elegance. Here’s why it stands out compared to Ansible, Terraform, or extending Docker Compose:

#### 1. Minimal Learning Curve

- **Straightforward Syntax**: Docpose utilizes YAML and Jinja2, which are relatively simple and easy to learn. Users familiar with basic YAML structure and Jinja2 templating can quickly get up to speed.
- **Focused Scope**: Unlike Ansible and Terraform, which cover a wide range of provisioning and orchestration tasks, Docpose is specifically designed for templating configurations. This narrow focus makes it easier to learn and use.

#### 2. Reduced Complexity

- **Single Purpose**: Docpose is designed solely for templating configuration files, reducing the cognitive load associated with multi-purpose tools like Ansible or Terraform.
- **No Additional Dependencies**: It doesn’t require setting up additional infrastructure or services, which is often the case with Terraform and Ansible.

#### 3. Clear and Reusable Configuration

- **Anchors and Aliases**: Docpose leverages YAML anchors and aliases to avoid redundancy and promote reuse, making configurations cleaner and more maintainable.
- **Template Context**: Each template can have its own context, allowing for fine-grained control over configurations without cluttering the main configuration file.

#### 4. Environment Management

- **Environment Variables**: Docpose allows you to manage environment variables directly within the configuration file. You can override variables for specific templates, making it flexible and reducing the need for external scripts or tools.
- **.env Support**: It supports `.env` files out-of-the-box, allowing you to separate configuration from code seamlessly.

#### 5. Dependency Management

- **Dependencies Between Templates**: Docpose’s `depends_on` feature allows you to define dependencies between templates, ensuring that configurations are generated in the correct order. This is simpler and more direct than managing task dependencies in Ansible.

#### 6. Lightweight and Portable

- **Python-Based**: Being a Python-based tool, it is lightweight and easy to install using `pip`. This portability makes it suitable for quick setup and integration into existing CI/CD pipelines.
- **Minimal Configuration Files**: Docpose configuration files are typically smaller and less complex than those required for Ansible playbooks or Terraform scripts.

### Comparison with Other Tools

#### Ansible

- **Use Case**: Ansible is designed for configuration management and application deployment.
- **Complexity**: Requires a deeper understanding of modules, playbooks, and roles. Managing complex dependencies and conditions can be cumbersome.
- **Setup**: Requires setting up an Ansible control node and managing SSH access to nodes.

#### Terraform

- **Use Case**: Terraform is used for infrastructure as code, managing cloud resources, and provisioning infrastructure.
- **Complexity**: Requires understanding of the HashiCorp Configuration Language (HCL) and managing state files. It’s overkill for simple templating tasks.
- **Setup**: Involves setting up providers, maintaining state files, and handling infrastructure provisioning.

#### Extending Docker Compose

- **Use Case**: Docker Compose is primarily used for defining and running multi-container Docker applications.
- **Complexity**: Extending Docker Compose for complex templating can become unwieldy. It lacks built-in support for environment variable management and conditional logic.
- **Setup**: Requires Docker and Docker Compose to be installed, and managing large `docker-compose.yml` files can be challenging.

### Conclusion

Docpose provides a more focused, simpler, and elegant solution for templating configurations compared to the broader scope and complexity of Ansible, Terraform, or extending Docker Compose. Its lightweight nature, clear syntax, and built-in support for environment and dependency management make it an ideal choice for developers seeking simplicity and elegance in their configuration management workflows.
