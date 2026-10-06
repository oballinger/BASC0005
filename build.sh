#!/bin/bash
# Build the course site: the book (index, workshop notebooks, slide pages) then the lecture decks.
# The book render cleans docs/, so the decks must be rendered after it.
set -e
cd "$(dirname "$0")"
quarto render --to html
(cd lectures/qmd && quarto render)   # decks (qmd/ is generated from PowerPoint by lectures/tools/sync.py)
