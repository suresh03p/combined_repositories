from transformers import pipeline


DEFAULT_MODEL = "distilgpt2"


def run_prediction(prompt: str, max_new_tokens: int = 32, temperature: float = 0.7, top_k: int = 50, top_p: float = 0.95, do_sample: bool = True):
    if prompt is None or not isinstance(prompt, str):
        raise ValueError("Input must be a string.")

    cleaned = prompt.strip()
    if not cleaned:
        raise ValueError("Input cannot be empty.")

    if len(cleaned) > 5000:
        raise ValueError("Input exceeds maximum character length.")

    generator = pipeline("text-generation", model=DEFAULT_MODEL, tokenizer=DEFAULT_MODEL)
    outputs = generator(
        cleaned,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=do_sample,
    )
    return outputs[0]["generated_text"]


if __name__ == "__main__":
    test_cases = [
        "Simple input: I cannot log into my account.",
        "Long input: " + ("This is a long request. " * 50),
        "",
        "   ",
        None,
    ]

    for case in test_cases:
        try:
            print("INPUT:", repr(case))
            result = run_prediction(case if isinstance(case, str) else "")
            print("OUTPUT:", result)
        except Exception as exc:
            print(f"ERROR: {exc}")
