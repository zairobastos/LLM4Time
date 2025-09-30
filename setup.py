import os
from setuptools import setup, find_packages


def get_version():
  with open(os.path.join(os.path.dirname(__file__), 'llm4time/version.py')) as f:
    exec(f.read(), globals())
  return globals()['__version__']


with open("README.md", "r") as arq:
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
          "lmstudio==1.3.0",
          "numpy>=1.23.0,<2.2.5",
          "openai>=1.40.0,<1.86.0",
          "openpyxl>=3.1.0,<3.2.0",
          "pandas>=2.0.0,<2.2.3",
          "permetrics>=1.5.0,<2.0.0",
          "plotly>=5.15.0,<6.1.0",
          "scikit-learn>=1.3.0,<1.7.1",
          "scipy>=1.10.0,<1.15.3",
          "statsmodels>=0.14.0,<0.14.5"
      ])
