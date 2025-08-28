# 📈 LLM4Time

**LLM4Time** é uma ferramenta interativa para previsão de séries temporais utilizando *Large Language Models* (LLMs). A aplicação permite o upload de arquivos CSV com séries temporais e gera previsões baseadas em diferentes tipos de *prompts*, automatizando etapas como tratamento de dados, seleção de janela temporal e visualização de resultados.

## 🚀 Demonstração

📽️ Assista à demonstração no YouTube: [LLM4Time - YouTube](https://youtu.be/fYSDC_mtjtI)  
📁 Repositório oficial: [github.com/zairobastos/LLM4Time](https://github.com/zairobastos/LLM4Time)

---

## 🧩 Funcionalidades

- Previsão de séries temporais com LLMs
- Upload de arquivos CSV personalizados
- Seleção de modelos e prompts
- Histórico de execuções com filtro por prompt/base
- Interface amigável via Streamlit

---

## ⚙️ Instalação

Siga os passos abaixo para clonar e executar o projeto localmente:

### 1. Clonar o repositório

```bash
git clone https://github.com/zairobastos/LLM4Time.git
cd LLM4Time
```

### 2. Criar e ativar ambiente virtual

```bash
virtualenv --creator venv venv --system-site-packages
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o banco de dados

```bash
python3 create_database.py
```

### 5. Executar a aplicação

```bash
python3 main.py
```

---

## 📝 Requisitos

- Python 3.9 ou superior
- `virtualenv` instalado

---

## 🧠 Autores

- **Zairo Bastos**  
- **Carlos Caminha**  
- **José Wellington Franco**

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📬 Contato

Em caso de dúvidas, sugestões ou feedback:

- 📧 Email: [zairobastos@gmail.com](mailto:zairobastos@gmail.com)
- 🔗 LinkedIn: [Zairo Bastos](https://www.linkedin.com/in/zairobastos/)