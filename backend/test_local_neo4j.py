import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import openai

# Load environment variables from .env file
load_dotenv()

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")  # Fixed variable name
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Debugging: Print to check if env variables are loaded
print(f"NEO4J_URI: {neo4j_uri}")
print(f"NEO4J_USER: {neo4j_user}")
print(f"NEO4J_PASSWORD: {neo4j_password}")
print(f"OPENAI_API_KEY: {'*' * len(openai.api_key) if openai.api_key else None}")


def query_neo4j(query):
    try:
        # driver = GraphDatabase.driver(neo4j_uri)
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            result = session.run("RETURN 'Connected to Neo4j!'")
            print(result.single()[0])  # Should print "Connected to Neo4j!"
    except Exception as e:
        print(f"Neo4j Connection Error: {e}")


# Ensure you use the new OpenAI client
client = openai.OpenAI()


def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return "Error in generating text."


# Example usage
neo4j_query = "MATCH (n) RETURN n LIMIT 5"
print(query_neo4j(neo4j_query))

# openai_prompt = "Write a short story about a robot learning to love."
# print(generate_text(openai_prompt))