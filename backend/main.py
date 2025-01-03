import os
import uvicorn
from application import create_app, FastAPI

app: FastAPI = create_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=os.environ.get('APP_HOST'),
        port=int(os.environ.get('APP_PORT')),
        reload=True
    )
