import json
from TexSoup import read
from TexSoup.data import TexNamedEnv, TexEnv, TexCmd
import argparse
import os
import re
from pathlib import Path
import ziamath as zm
import cairosvg

from dataclasses import dataclass

counter = 1
latex_store = None

def latex_to_png(expr_str, output_path):
  expr = zm.Latex(expr_str, color='white')
  png_bytes = cairosvg.svg2png(expr.svg())
  with open(output_path, 'wb') as f:
    f.write(png_bytes)


def convert_latex(text, output_dir, counter):
  print(output_dir)
  filename = f"equ{counter}.png"
  filepath = os.path.join(output_dir, filename)
  latex_to_png(text, filepath)
  counter += 1
  return f"{{image=latex/{filename}}}", counter

@dataclass
class Macro:
  name: str
  contents: list
  args: list

@dataclass
class Env:
  name: str
  code: any

def demacro(node) -> Macro:
  # print("contents:", node.contents)
  # print("args:", node.args)
  return Macro(
      name= node.name,
      args= list(map(lambda x: x.contents[0], node.args)),
      contents= list(map(lambda x:deconstruct(x), node.contents))
      # args= list(map(lambda x: x.contents[0], node.args))
  )
  # return {
  #   "macro": node.name,
  #   "args": list(map(lambda x: x.contents[0], node.args))
  # }

def deconstruct(node):
  # is macro
  if(isinstance(node, TexCmd)):
    return demacro(node)

  # is not macro and env
  if(not isinstance(node, TexEnv) and not isinstance(node, TexNamedEnv)):
    # ignore if comments
    if(str(node)[0] == "%"): return ""
    return str(node).replace("\\\\","")

  code = ""
  if node.name == "$" or node.name == "$$" or "equation" in node.name:
    code = "".join(map(str, node.contents[0:])).strip()
  else:
    code = list(map(deconstruct,node.contents[0:]))

  return Env(
    name=node.name,
    code=code
  )

  # return {
  #   "env": node.name,
  #   "code": code
  # }

def character_said(name, emotion, code):
    deeped = map(deep, code)
    joinned = "".join(list(deeped))
    striped = "".join(list(map(lambda x: x.strip(), joinned.split("\n"))))
    return f'\n    show {name} {emotion}\n    {name} "{striped}"\n'

def deep_in_macro(node):
  if(node.name == "textbf"): return f'**{node.args[0]}**'
  if(node.name == "footnote"): return f"({node.args[0]})\n"
  if(node.name == "item"):
    deeped = map(deep, node.contents)
    joinned = "".join(list(deeped))
    striped = "".join(list(map(lambda x: x.strip(), joinned.split("\n"))))
    return "* " + striped + "\n"
  return f"\n    # (undefined macro: {node.name})\n"

def deep_in_env(node):
  global counter, latex_store
  # handling inline and line equations
  # if(node.name == "$"): return f'${node.code}$'
  # if(node.name == "$$"): return f'$${node.code}$$'
  # if("equation" in node.name): return f'$${node.code}$$'

  if("$" in node.name or "equation" in node.name):
    print("code: ", node.code)
    print("num: ", counter)
    processed_text, counter = convert_latex(node.code, latex_store, counter)
    print("latex: ", processed_text)
    print("=" *20)
    return processed_text

  if(node.name == "teacherSaid"): return character_said("b", "talking", node.code)
  if(node.name == "readerSaid"): return character_said("a", "agree", node.code)

  if(("teacher" in node.name or "reader" in node.name) and "Env" in node.name):
    emotion = node.name.replace("teacher", "").replace("reader", "").replace("Env", "").lower()
    character_name = "b" if "teacher" in node.name else "a"
    return character_said(character_name, emotion, node.code)

  if("Figure" in node.name): return f"\n    #({node.name})"
  if(node.name == "comment"): return ""

  res = list(map(deep, node.code))
  return "\n    "+"".join(res)

def deep(node):
  if(isinstance(node, str)):
    return node

  if(isinstance(node, Env)): return deep_in_env(node)
  if(isinstance(node, Macro)): return deep_in_macro(node)

def main():
  global latex_store
  parser = argparse.ArgumentParser(description="Convert Markdown + LaTeX to Ren'Py script")
  parser.add_argument('--latex-store', required=True, help='Path to store LaTeX PNGs')
  parser.add_argument('--input', required=True, help='Input Flatten Tex file')
  parser.add_argument('--output', required=True, help='Output Ren\'Py script file')
  args = parser.parse_args()

  Path(args.latex_store).mkdir(parents=True, exist_ok=True)

  with open(args.input, encoding="utf-8") as f:
    source_code = f.read()

  soup, _ = read(source_code)

  latex_store = args.latex_store

  renpy_script = "label book:\n\n"
  renpy_script += deep(deconstruct(soup))

  with open(args.output, "w", encoding="utf-8") as f:
    f.write(renpy_script)

  print(f"Conversion complete! Output saved to {args.output}")

if __name__ == "__main__":
    main()
