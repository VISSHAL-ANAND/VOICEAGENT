from fastapi import FastAPI

app = FastAPI(title='VoiceAgent API')

@app.get('/healthz')
def health():
    return {'status': 'ok', 'mode': 'local-mock'}
