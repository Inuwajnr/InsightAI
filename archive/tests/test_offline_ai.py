import pandas as pd

from data.offline_ai import OfflineAIEngine


df = pd.DataFrame({
    "Product": [
        "Laptop",
        "Phone",
        "Laptop",
        "Tablet",
        "Phone",
        "Monitor",
    ],
    "Category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "Electronics",
        "Electronics",
        "Electronics",
    ],
    "Quantity": [
        5,
        12,
        8,
        6,
        10,
        4,
    ],
    "Unit Price": [
        500000,
        300000,
        500000,
        250000,
        300000,
        200000,
    ],
    "Region": [
        "North",
        "South",
        "North",
        "West",
        "South",
        "West",
    ],
})


ai = OfflineAIEngine()


print("=" * 60)
print("        INSIGHTAI HYBRID OFFLINE AI TEST")
print("=" * 60)
print()
print("Dataset:")
print(df)
print()


while True:

    question = input("You: ").strip()

    if question.lower() in [
        "exit",
        "quit",
    ]:
        print("Goodbye!")
        break

    if not question:
        continue

    print()
    print("InsightAI:")
    print()

    answer = ai.answer(
        df,
        question,
    )

    print(answer)
    print()