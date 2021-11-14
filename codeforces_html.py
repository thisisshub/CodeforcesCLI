from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
import typer
import requests


app = typer.Typer()

pd.options.mode.chained_assignment = None


tags = ["implementation", "math", "greedy", "dp", "data structures",
        "brute force", "constructive algorithms", "graphs", "sortings",
        "binary search", "dfs", "dfs and similar", "trees", "strings",
        "number theory", "combinatrics", "geometry", "bitmasks", "two pointers",
        "dsu", "shortest paths", "probabilities", "divide and conquer",
        "hashing", "games", "flows", "interactive", "matrices", "string suffix structures",
        "fft", "graph matchings", "ternary search", "expression parsing", "meet-in-the-middle",
        "2-sat", "chinese remainder theorem", "schedules"]

def to_clean_name(s: str, tags: list) -> str:
    """Returns clean name
    Eg: Blue-Red Permutation greedy, math, sortings -> Blue-Red Permutation
    """
    chars_to_remove = [',', '!', '?', '.']
    s = ''.join([c for c in s if c not in chars_to_remove])
    s = list(s.split())
    return ' '.join([c for c in s if c not in tags])


@app.command()
def latest(df):
    """Returns the latest problemset from codeforces.com/problemset
    """
    url = "https://codeforces.com/problemset/"
    df = pd.read_html(url)
    df = df[0].dropna(axis='columns', how='all')
    for i in df.Name:
        df.Name[df.Name==i] = to_clean_name(i, tags)
    print(df.to_string())


@app.command()
def pb(problem: str):
    """Returns content of a requested problem
    """
    url = "https://codeforces.com/problemset/problem/"
    updated_url = url + problem[:-1] + "/" + problem[-1:].upper()
    r = requests.get(updated_url)
    soup = bs(r.content, 'html5lib')
    content = soup.find('div', attrs = {'class' : 'ttypography'})
    for div in content.findAll('div', attrs = {'class' : 'problem-statement'}):
        dic = {}
        header = div.find(class_="header")
        dic["title"] = header.find(class_="title").get_text()
        dic["time_limit"] = header.find(class_="time-limit").get_text()
        dic["memory_limit"] = header.find(class_="memory-limit").get_text()
        dic["text"] = div.find("p").get_text()
        dic["input_specification"] = div.find(class_="input-specification").find("p").get_text()
        dic["output_specification"] = div.find(class_="output-specification").find("p").get_text()

        # Get actual input and output
        sample_tests = div.find(class_="sample-tests")
        _list = []
        for i, o in sample_tests.findAll(class_="input"), sample_tests.findAll(class_="output"):
            _list.append([i.find("pre").get_text(), o.find("pre").get_text()])
        io_dict = dict(zip(_list[0], _list[1]))
        #io_dict["input"] = sample_tests.find(class_="input").find("pre").get_text()
        #io_dict["output"] = sample_tests.find(class_="output").find("pre").get_text()
    print(dic, io_dict)


if __name__ == "__main__":
    app()
