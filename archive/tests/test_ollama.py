from core.ollama_client import OllamaClient


ai = OllamaClient()

print("=" * 60)
print("INSIGHTAI OLLAMA TEST")
print("=" * 60)

question = input("You: ")

try:
    answer = ai.generate(question)

    print()
    print("Qwen3:")
    print(answer)

except Exception as e:
    print()
    print("ERROR:")
    print(e)