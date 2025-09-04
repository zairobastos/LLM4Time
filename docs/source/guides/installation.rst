Instalação
==========

Instalação via pip:

.. code-block:: bash

  pip install llm4time

Além disso, disponibilizamos uma interface via Streamlit, proporcionando uma interação mais intuitiva e prática com a biblioteca.

Siga os passos abaixo para clonar o repositório, configurar o ambiente e executar a aplicação.

**1. Clone o repositório**

.. code-block:: bash

  git clone https://github.com/zairobastos/LLM4Time.git
  cd LLM4Time

**2. Crie e ative um ambiente virtual (Opcional)**

.. code-block:: bash

  python -m venv venv
  source venv/bin/activate      # Bash/Zsh
  source venv/bin/activate.fish # Fish Shell

**3. Instale as dependências**

.. code-block:: bash

  python -m pip install --upgrade pip
  pip install -r requirements.txt -r requirements-streamlit.txt

**4. Execute a aplicação**

Usando python:

.. code-block:: bash

  python app/main.py

Ou usando docker:

.. code-block:: bash

  docker compose up
