from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Definition:
    """Represents a function, method, or class definition."""
    name: str
    type: str  # 'function', 'method', or 'class'
    module: str
    class_name: str = None
    start_line: int = None
    end_line: int = None


@dataclass
class Module:
    """Represents a parsed Python module."""
    definitions: dict[str, Definition] = field(default_factory=dict)  # {qualified_name: Definition}
    calls: defaultdict[str, list[str]] = field(default_factory=lambda: defaultdict(list))  # {caller: [callees]}
    imports: dict[str, str] = field(default_factory=dict)  # {imported_name: original_module}


@dataclass
class Class:
    """Represents a function, method, or class definition."""
    name: str
    module: str
    methods: list[Definition] = None
