from dataclasses import dataclass

LAYER_COGNITIVE = "cognitive"
LAYER_PHYSICS = "physics"


@dataclass(frozen=True)
class Engine:
    id: int
    codename: str
    layer: str
    full_name: str
    description: str
    negative_pole: str
    positive_pole: str


ENGINES = [
    Engine(1, "GRAVITON", LAYER_COGNITIVE, "Gravity Escape",
           "Escape the generic median.", "bland", "memorable"),
    Engine(2, "ANCHOR", LAYER_COGNITIVE, "Reality Anchor",
           "Tie claims to evidence.", "hand-waving", "source-anchored"),
    Engine(31, "ENTROPY", LAYER_PHYSICS, "Entropy Gate", "Hard state gate.", "collapse", "order"),
    Engine(n, "NOT_CONSTANT", LAYER_PHYSICS, "Dynamic", "Skipped: first arg is not a literal.", "a", "b"),
]
