from neo4j import GraphDatabase

uri = "neo4j+s://e934d3f2.databases.neo4j.io"  # or your specific URI
username = "neo4j"
password = "anZIZv9LaYXXqYq7xRSwAr-pqDy7zxFQepUZzR5WXyw"

# NEO4J_URI=neo4j+s://e934d3f2.databases.neo4j.io
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=anZIZv9LaYXXqYq7xRSwAr-pqDy7zxFQepUZzR5WXyw

driver = GraphDatabase.driver(uri, auth=(username, password))
print("Checking")

def test_connection():
    with driver.session() as session:
        return session.run("RETURN 1").single()[0]

try:
    result = test_connection()
    print("Connected successfully, returned:", result)
except Exception as e:
    print("Failed to connect:", e)