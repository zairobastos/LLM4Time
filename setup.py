import os
from setuptools import setup, find_packages


def get_version():
  with open(os.path.join(os.path.dirname(__file__), 'llm4time/version.py')) as f:
    exec(f.read(), globals())
  return globals()['__version__']


with open("README.md", "r", encoding="utf-8") as arq:
  readme = arq.read()


version = get_version()

setup(name="llm4time",
      version=version,
      license="MIT License",
      author="Zairo Bastos",
      author_email="zairobastos@gmail.com",
      url="https://github.com/zairobastos/LLM4Time",
      long_description=readme,
      long_description_content_type="text/markdown",
      keywords=[
          "time series",
          "forecasting",
          "LLM",
          "large language models"
      ],
      description="Um pacote para previsão de séries temporais usando modelos de linguagem.",
      python_requires=">=3.10",
      packages=find_packages(),
      install_requires=[
          "openpyxl>=3.1.0,<3.2.0",
          "numpy>=1.23.0,<2.3.0",
          "pandas>=2.0.0,<2.3.0",
          "permetrics>=2.0.0,<2.1.0",
          "plotly>=6.1.0,<6.2.0",
          "scikit-learn>=1.7.1,<1.8.0",
          "scipy>=1.15.3,<1.16.0",
          "statsmodels>=0.14.5,<0.15.0"
      ])
