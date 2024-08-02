from typing import List, Dict
from dataclasses import dataclass, field
from colorama import Fore, Style, init

init(autoreset=True)

@dataclass
class KeyValueMessage:
    variable_key: str
    variable_value: str
    message: str
    rule_name: str

@dataclass
class WarningEntry:
    template: str
    key_value_messages: List[KeyValueMessage] = field(default_factory=list)

warnings: Dict[str, WarningEntry] = {}

def warn(template: str, rule_name: str, rules: Dict[str, str], message: str):
    if template not in warnings:
        warnings[template] = WarningEntry(template=template)
    
    entry = warnings[template]
    for key, value in rules.items():
        entry.key_value_messages.append(KeyValueMessage(variable_key=key, variable_value=value, message=message, rule_name=rule_name))

def print_warnings():
    # Calculate maximum widths for dynamic formatting
    max_key_width = max(len(kv_message.variable_key) for entry in warnings.values() for kv_message in entry.key_value_messages)
    max_value_width = max(len(kv_message.variable_value) for entry in warnings.values() for kv_message in entry.key_value_messages)
    max_rule_width = max(len(kv_message.rule_name) for entry in warnings.values() for kv_message in entry.key_value_messages)
    max_message_width = max(len(kv_message.message) for entry in warnings.values() for kv_message in entry.key_value_messages)

    # Calculate padding for alignment
    key_value_padding = max_key_width + max_value_width + 5  # Padding between key-value and message

    # Print header
    print(f"\n{Fore.YELLOW}#############################{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}###### DOCPOSE WARNING ######{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}#############################{Style.RESET_ALL}\n")

    # Print warnings
    for template, entry in warnings.items():
        print(f'{Fore.LIGHTCYAN_EX}{template}{Style.RESET_ALL}')
        for kv_message in entry.key_value_messages:
            # Print formatted output with dynamic widths
            print(
                f" * {Fore.LIGHTMAGENTA_EX}{kv_message.variable_key:<{max_key_width}}{Fore.RESET}   "
                f"{Fore.LIGHTGREEN_EX}{kv_message.variable_value:<{max_value_width}}{Fore.RESET}    "
                f"{Fore.LIGHTYELLOW_EX}{kv_message.rule_name:<{max_rule_width}}{Style.RESET_ALL}  "
                f"{Fore.RED}{kv_message.message.ljust(max_message_width)}{Style.RESET_ALL}"
            )