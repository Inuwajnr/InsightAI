from openai import OpenAI


client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Reply with exactly: InsightAI API connection successful."
)

print(response.output_text)