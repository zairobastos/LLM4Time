import os
import glob
import subprocess
from utils.paths import abspath

# LLM4Time
from llm4time.persistence.create_database import create_database


def run():
  os.makedirs(abspath("uploads"), exist_ok=True)
  os.makedirs(abspath("database"), exist_ok=True)

  if not glob.glob(abspath("database/*.db")):
    create_database(abspath("database/database.db"))

  subprocess.run(["streamlit", "run", abspath("app.py")])


if __name__ == "__main__":
  run()
