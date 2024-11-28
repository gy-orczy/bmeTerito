import ollama

response = ollama.chat(
    model='phi3.5',
    messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue? REPLY IN ONE SENTENCE!!!',
        },
    ]
)

# Corrected print statement
print(response['message']['content'])
