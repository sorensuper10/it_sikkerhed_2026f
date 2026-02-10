import uvicorn
from Softwaresikkerhed10022026.flat_file.rest_api import Rest_api

api = Rest_api(database_file_name="./src/db_flat_file.json")
app = api.app

if __name__ == "__main__":
    uvicorn.run("Softwaresikkerhed10022026.flat_file.main:app", host="127.0.0.1", port=8000, reload=True)