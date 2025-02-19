from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = "Gyan"    
SCR_REPO = "src"
LIST_OF_REQUIREMENTS = ["streamlit"]

setup(
    name = SCR_REPO,
    version = "0.0.1",
    author = AUTHOR_NAME,
    author_email = "gyankumar2431@gmail.com",
    description = "Movie Recommendation System",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    package = [SCR_REPO],
    python_requires = ">=3.6",
    install_requires = LIST_OF_REQUIREMENTS
)