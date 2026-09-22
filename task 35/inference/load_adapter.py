import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel


def load_customized_model(base_model: str = "distilgpt2", adapter_path: str = "./models/day30_adapter"):
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    base = AutoModelForCausalLM.from_pretrained(base_model)

    model = PeftModel.from_pretrained(base, adapter_path)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    return tokenizer, model, pipe


if __name__ == "__main__":
    base_model = os.getenv("BASE_MODEL_NAME", "distilgpt2")
    adapter_path = os.getenv("ADAPTER_PATH", "./models/day30_adapter")
    tokenizer, model, pipe = load_customized_model(base_model, adapter_path)

    prompt = "I cannot log into my account."
    result = pipe(prompt, max_new_tokens=25, do_sample=False)[0]["generated_text"]
    print("Tokenizer loaded successfully")
    print("Model loaded successfully")
    print("Prediction:", result)
