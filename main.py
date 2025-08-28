import os
import subprocess

class Main:
  def __init__(self):
    pass

  def run(self):
    os.makedirs("database", exist_ok=True)
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
  Main().run()
