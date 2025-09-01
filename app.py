from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>Prover9 Online</title>
<h1>Enter axioms (Prover9 format)</h1>
<form method=post>
  <textarea name=axioms rows=15 cols=80></textarea><br>
  <input type=submit value="Run Prover9">
</form>
{% if output %}
<h2>Output:</h2>
<pre>{{ output }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        axioms = request.form["axioms"]
        with open("./input.p9", "w") as f:
            f.write(axioms)
        try:
            result = subprocess.run(
                ["prover9", "-f", "input.p9"],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout + "\n" + result.stderr
            print(0, output)
        except Exception as e:
            print(1, str(e))
            output = str(e)
    return render_template_string(HTML_PAGE, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7654)
