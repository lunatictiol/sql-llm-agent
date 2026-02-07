from enum import Enum

class ModelType(str, Enum):
    QWEN = "qwen2.5-7b"
    PHI = "phi-3"
    LLAMA3 = "llama3"
