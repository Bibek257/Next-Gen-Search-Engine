from flask import Flask, render_template, request
from main import agent_node  # Your agent code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer, sources = None, None
    if request.method == "POST":
        query = request.form.get("query")
        state = {"query": query}
        result = agent_node(state)
        answer = result.get("answer")
        sources = result.get("sources", "")
    return render_template("index.html", answer=answer, sources=sources)

if __name__ == "__main__":
    app.run(debug=True)
