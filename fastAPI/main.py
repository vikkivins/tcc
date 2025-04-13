import uvicorn
from api import app

# Inicie o servidor com o Uvicorn (caso execute diretamente o script)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)