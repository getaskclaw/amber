"""adapter 注册表。"""
from . import openai_baseline, openrouter, typesafe_native

ADAPTERS = {
    "typesafe-native": typesafe_native,
    "openrouter": openrouter,
    "openai-compatible-baseline": openai_baseline,
}
