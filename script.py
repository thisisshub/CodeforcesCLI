from codeforces_html import codeforces_html, to_get_latest_problem_set
import typer
import pandas as pd

app = typer.Typer()


@app.command()
def hello():
    print("Hello")


@app.command()
def goodbye():
    print("Goodbye")


@app.command()
def problemset():
    print(to_get_latest_problem_set)


if __name__ == "__main__":
    app()

