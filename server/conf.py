import os
from glide.conf import *

# -- Project information -----------------------------------------------------

project = "Secret Pico"
# noinspection PyShadowingBuiltins
copyright = 'Joel Burton and Fluffy Labs'
author = 'Joel Burton'

# The short X.Y version
version = os.environ.get("RITHM_COHORT")
# The full version, including alpha/beta/rc tags
release = f'March 2021'

# -- General configuration ---------------------------------------------------

# RST Prolog: this stuff is added to every RST file before it's processed
_curric_name = f"""
.. |curric-name|   replace:: {os.environ.get('CURRIC_NAME')}
"""

rst_prolog += _curric_name

# -- Options for HTML output -------------------------------------------------

# revealjs_theme = "revealjs-rithm"
# html_theme = "handouts-rithm"

# -- Extension configuration -------------------------------------------------

# If false, the to-do and to-do-list directives produce nothing
todo_include_todos = True
