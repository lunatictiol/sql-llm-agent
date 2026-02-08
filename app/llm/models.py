from enum import Enum

class ModelType(str, Enum):
    QWEN = "qwen2.5-coder"
    PHI = "phi3"
    LLAMA3 = "llama3"
