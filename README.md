# latex_renpy

> This tool is work in progress.

A tool convert [my template](https://github.com/ljcucc/math_note_template)'s latex note into renpy script

## Create VN(Visual Novel) with your note - Ren'Py

Interactive note is fun, but how?

Things you'll need to prepare for creating a visual novel:

* Generate diagrams
* Generate latex formula
* Generate scripts (combine assets togather)

### Convert your note assets to renpy format

renmae `a-emotion.png` to `a emtion.png` for renpy format.

```sh
for f in *-*.png; do
mv "$f" "${f/-/ }"
done
```

### Convert note source code ren'py script

use `latex-flatten` to flatten your tex.

```sh
pip install latex-flatten
python3 -m latex-flatten ./main.tex --outdir FLATTENED
```

and convert your flattened latex to renpy script:

```sh
python3 ./latex_renpy.py --output ..somewhere/game/book.rpy --input .your/main.tex --latex-store ..somewhere/game/images/latex
```
