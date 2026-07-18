from fastapi import FastAPI
app= FastAPI()

@app.get('/')
def index():
    return{
        "message":"hello flyrank!!"
    }

@app.get('/health')

def health():
    return{
        "message":"ok"
    }
    