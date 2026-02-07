from setuptools import setup, find_packages

setup(
    name="diminishing-returns",
    version="0.0.0",
    description="Diminishing returns meter for multi-agent / multi-LLM conversations (stop/ship signal, not confidence).",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={"console_scripts": ["dr=dr.cli:main"]},
)
