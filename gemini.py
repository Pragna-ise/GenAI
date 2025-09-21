import vertexai
from vertexai.generative_models import GenerativeModel

# Init Vertex AI with project + region
vertexai.init(project="legall-472707", location="us-central1")

# Use correct model name
model = GenerativeModel("gemini-2.5-pro")  # or "gemini-1.5-pro-001"

prompt = "Summarize this clause: Tenant must pay a penalty of 3 months rent if lease is broken."
response = model.generate_content(prompt)

print(response.text)
