# latex_renpy

> This tool is work in progress.

A tool convert [my template](https://github.com/ljcucc/math_note_template)'s latex note into renpy script

## Create VN(Visual Novel) with your note - Ren'Py

Steps to create Ren'Py script from your tex file:

1. Flatten your tex file.
2. Convert latex formula into png, and generate rpy script file.
3. Transfer assets from note to game

### 1. Flatten your tex file

To create a flattened latex script, please avoid standalone package while doing this script. for [my template](https://github.com/ljcucc/math_note_template), try to create an extra file to `\input` or `\include` your notes, for example:

```
\input{your-script.tex}
\input{your-script-2.tex}
\input{your-script-3.tex}
```

use `latex-flatten` to flatten your tex.

```sh
pip install latex-flatten
python3 -m latex-flatten ./main.tex --outdir FLATTENED
```

### 2. convert your flattened latex to renpy script:


```sh
python3 ./latex_renpy.py --output ..somewhere/game/book.rpy --input .your/main.tex --latex-store ..somewhere/game/images/latex
```

###  3. Transfer assets from note to game

This step is designed for [my template](https://github.com/ljcucc/math_note_template), which will convert your note assets to renpy format.

renmae `a-emotion.png` to `a emtion.png` for renpy format.

```sh
for f in *-*.png; do
mv "$f" "${f/-/ }"
done
```
