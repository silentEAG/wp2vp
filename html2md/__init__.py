from bs4 import BeautifulSoup
from urllib.parse import unquote

global is_tag


def render2md(el):
    if el is None:
        return ""
    if el.parent is None:
        return el

    tag = el.parent
    if tag.name == 'a':
        pre = ""
        if (tag.next_sibling == "\n" or tag.next_sibling is None) and tag.parent.name != 'li':
            pre += "\n"
        if el == tag['href'] and (tag.parent is not None and tag.parent.name != 'li'):
            pre += "- "
        return f"{pre}[{unquote(el, 'utf-8')}]({tag['href']})"
    elif tag.name == 'img':
        return f"![{tag['src']}]({el}) "
    elif tag.name == 'h1':
        return f"# {el}"
    elif tag.name == 'h2':
        return f"## {el}"
    elif tag.name == 'h3':
        return f"### {el}"
    elif tag.name == 'h4':
        return f"#### {el}"
    elif tag.name == 'code' and tag.parent.__class__ == is_tag and tag.parent.name == 'pre':
        if isinstance(tag.get('class'), list):
            return f"```{tag.get('class')[0].split('-')[1]}\n{el}\n```"
        else:
            return f"```\n{el}\n```"
    elif tag.name == 'code':
        return f"`{el}`"
    else:
        return el


def pre_render(tag):
    if tag.name == "li":
        return "- "
    elif tag.name == "img":
        return f"![]({tag['src']})"
    else:
        return ""


def dfs(el):
    if el.__class__ != is_tag or el is None:
        return render2md(el)
    # print(el.name)
    # print(el.contents)
    res = ""
    for el_ch in el.children:
        # print(el_ch)
        if el_ch.__class__ == is_tag:
            if el.name == "body":
                res += "\n"
            res += pre_render(el_ch) + dfs(el_ch)
        else:
            res += render2md(el_ch)
    return res


def work_from_html_to_md(content):
    if "<!-- /wp:" in content:
        return ""
        # raise Exception("This method does not support wordpress native format!")
    global is_tag
    soup = BeautifulSoup(content, 'lxml')
    is_tag = soup.body.__class__
    resp = dfs(soup.body)
    return resp
