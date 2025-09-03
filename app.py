from flask import Flask, request, redirect, url_for, render_template, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = "supersecret"
FILES_DIR = "./prover9_files"
os.makedirs(FILES_DIR, exist_ok=True)


@app.route("/")
def index():
    files = [f for f in os.listdir(FILES_DIR) if f.endswith(".p9")]
    return render_template("index.html", files=files)


@app.route("/new", methods=["GET", "POST"])
def new_file():
    files = [f for f in os.listdir(FILES_DIR) if f.endswith(".p9")]

    if request.method == "POST":
        filename = request.form["filename"].strip()
        if not filename.endswith(".p9"):
            filename += ".p9"
        filepath = os.path.join(FILES_DIR, filename)
        if os.path.exists(filepath):
            flash("File already exists!")
        else:
            with open(filepath, "w") as f:
                f.write(request.form["content"])
            flash(f"File {filename} created!")
        return redirect(url_for("index"))
    return render_template("new.html", files=files)


@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit_file(filename):
    filepath = os.path.join(FILES_DIR, filename)
    if request.method == "POST":
        with open(filepath, "w") as f:
            f.write(request.form["content"])
        flash(f"File {filename} updated!")
        return redirect(url_for("index"))
    with open(filepath) as f:
        content_text = f.read()
    files = [f for f in os.listdir(FILES_DIR) if f.endswith(".p9") and f != filename]
    return render_template("edit.html", filename=filename, content=content_text, files=files)


@app.route("/delete/<filename>")
def delete_file(filename):
    filepath = os.path.join(FILES_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"Deleted {filename}")
    return redirect(url_for("index"))


@app.route("/run/<filename>")
def run_file(filename):
    filepath = os.path.join(FILES_DIR, filename)
    try:
        result = subprocess.run(
            ["prover9", "-f", filepath],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + "\n" + result.stderr
    except Exception as e:
        output = str(e)
    return render_template("run.html", filename=filename, output=output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7654, debug=True)
