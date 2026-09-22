from transformers import AutoTokenizer


def demo_tokenizer(model_name='google/flan-t5-small'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    samples = [
        'Short sentence.',
        'This is a much longer sentence with more words and more complex language used in real customer support conversations.',
        '1234567890',
        'Hello, world! How are you?',
        'API timeout error on invoice service after payment retry.',
        'Hola, necesito ayuda con mi cuenta y mi pago.',
    ]

    for text in samples:
        ids = tokenizer(text, add_special_tokens=True)['input_ids']
        print(f'Text: {text}')
        print(f'  Tokens: {len(ids)}')
        print(f'  Token IDs: {ids[:10]}')
        print()


if __name__ == '__main__':
    demo_tokenizer()
