from setuptools import setup, find_packages

setup(
  name='lm_series_temporais',
  version='0.1',
  packages=find_packages(where='src'),
  package_dir={'': 'src'},
  install_requires=[
    'pandas',
    'numpy',
    'permetrics',
    'scipy',
  ],
  author='Zairo Bastos',
  author_email='zairobastos@gmail.com',
  description='Um pacote para previsão de séries temporais usando modelos de linguagem.'
)
