from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any


@dataclass
class EnvCondition:
    toContain: Optional[str] = None
    toEqual: Optional[str] = None
    toBeLoE: Optional[int] = None
    toBeGoE: Optional[int] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclass
class Source:
    template_dir: Optional[str] = ".python/templates"
    outputs: Optional[Union[str, List[str]]] = ".compose.yml"
    env_files: List[str] = field(
        default_factory=list,
        metadata={
            "description": "List of environment files. Optional, but required if 'environment' is not set."
        },
    )
    environment: List[str] = field(
        default_factory=list,
        metadata={
            "description": "List of environment variables. Optional, but required if 'env_files' is not set. Overrides the envs in files. Format: VAR_NAME: $SYSTEM_VAR or VAR_NAME: value."
        },
    )


@dataclass
class Compose:
    template: str
    output: Optional[str] = None
    depends_on: List[str] = field(
        default_factory=list,
        metadata={
            "description": "List of templates that this service depends on. Can reference other templates or system variables."
        },
    )
    env_files: List[str] = field(
        default_factory=list,
        metadata={
            "description": "List of environment files for this service. Optional."
        },
    )
    environment: List[Union[Dict[str, Union[str, int]], EnvCondition]] = field(
        default_factory=list,
        metadata={
            "description": "List of environment variables for this service. Optional. Overrides the envs in files. Format: VAR_NAME: $SYSTEM_VAR or VAR_NAME: value. Can also be a dictionary with conditions."
        },
    )


@dataclass
class Config:
    source: Source
    compose: List[Compose] = field(
        default_factory=list,
        metadata={
            "description": "List of compose objects or templates for Docker Compose."
        },
    )

    def __post_init__(self):
        # We do not need to do anything here for extra properties
        # The extra properties are implicitly allowed and ignored
        pass

    def __init__(self, source: Source, compose: List[Compose] = None, **kwargs: Any):
        # Initialize the base dataclass fields
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "compose", compose if compose is not None else [])

        # Handle extra properties (but do nothing with them in this case)
        # They are implicitly ignored
        self.extra_properties = kwargs
