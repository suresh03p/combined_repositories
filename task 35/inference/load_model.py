import os
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_base_model(model_name: str = "distilgpt2"):
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Tokenizer loaded successfully")

    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Model loaded successfully")

    return tokenizer, model


if __name__ == "__main__":
    model_name = os.getenv("MODEL_NAME", "distilgpt2")
    tokenizer, model = load_base_model(model_name)
    print(f"Tokenizer type: {type(tokenizer).__name__}")
    print(f"Model type: {type(model).__name__}")
