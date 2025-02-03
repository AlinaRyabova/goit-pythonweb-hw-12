import os
import sys
sys.path.insert(0, os.path.abspath('../src'))  # Додаємо шлях до каталогу src

extensions = [
    'sphinx.ext.autodoc',  # Автоматичне документування модулів
    'sphinx.ext.viewcode',  # Додає посилання на вихідний код
    'sphinx.ext.napoleon',  # Підтримка Google- та NumPy-стилю docstrings
]



# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'goit-pythonweb-hw-12'
copyright = '2025, R_Alina_V'
author = 'R_Alina_V'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
