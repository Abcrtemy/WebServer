import os
from jose import JWTError, jwt
import fastapi
import datetime
import json
from model import NoteItem

api_router = fastapi.APIRouter()

SECRET_KEY = 'c1a4f9a6172560bfe2e2ca95e6d72af14ed46f8a77e1960e2a41404853e566f7'
ALGORITHM = "HS256"

@api_router.get("/note/{noteId}", response_model=object)
async def getNote(noteId: str, token: str):
    verify_token_data = await verify_token(token)

    if verify_token_data == False: return {'error': 'Ошибка получения заметки (token)'}

    try:
        with open(f'data/{noteId}.json') as json_file:
            data = json.load(json_file)
    except EnvironmentError:
        return {'error': 'Ошибка получения заметки'}

    return json.loads(data)

@api_router.put("/note/{noteId}", response_model=None)
async def getNote(noteId: str, textData: fastapi.Request, token: str):
    verify_token_data = await verify_token(token)

    if verify_token_data == False: return {'error': 'Ошибка изменения заметки (token)'}

    try:
        req_text = await textData.body()

        with open(f'data/{noteId}.json') as json_file:
            data = json.load(json_file)

        oldData = json.loads(data)
        dateNow = datetime.datetime.now()

        response = NoteItem(
            created_at=oldData['created_at'],
            updated_at=dateNow,
            text=req_text,
            id=oldData['id']
        )

        with open(f'data/{noteId}.json', 'w') as write_file:
            json.dump(response.json(), write_file)

    except:
        return {'error': 'Ошибка изменения заметки'}

    return response
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjoic2VjcmV0IGluZm9ybWF0aW9uIiwiZnJvbSI6IkdGRyIsImV4cCI6MTcwMTY5OTU5Mn0.8F_k6xALOaQrN-hDc3etILxs4ldJfNeIBfurrMp-KPg
@api_router.delete("/note/{noteId}", response_model=str)
async def getNote(noteId: str, token: str):
    verify_token_data = await verify_token(token)

    if verify_token_data == False: return 'Ошибка удаления заметки (token)'

    try:
        os.remove(f'data/{noteId}.json')
    except OSError:
        return 'Ошибка удаления заметки'

    return 'Заметка успешно удалена!'

@api_router.get("/allNotes", response_model=None)
async def getAllNotes(token: str):
    verify_token_data = await verify_token(token)

    if verify_token_data == False: return {'error': 'Ошибка получения всех заметок (token)'}

    try:
        allNotes = []

        for subdir, dirs, files in os.walk("data"):
            for file in files:
                filepath = subdir + os.sep + file

                with open(filepath) as json_file:
                    data = json.load(json_file)

                id = json.loads(data)['id']

                allNotes.append(id)
    except:
        return 'Ошибка получения всех заметок'

    return allNotes

@api_router.post("/newNote/", response_model=None)
async def newNote(text: fastapi.Request, token: str):
    verify_token_data = await verify_token(token)

    if verify_token_data == False: return {'error': 'Ошибка создания заметки (token)'}

    try:
        req_text = await text.body()
        dateNow = datetime.datetime.now()

        response = NoteItem(
            created_at=dateNow,
            updated_at=dateNow,
            text=req_text,
            id=dateNow
        )

        with open(f'data/{str(dateNow.strftime("%Y%m%d-%H%M%S"))}.json', 'w') as write_file:
            json.dump(response.json(), write_file)

    except:
        return 'Ошибка создания заметки'

    return response


def create_access_token(data: dict):
    from datetime import datetime, timezone, timedelta

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@api_router.get("/get_token")
async def get_token():
    # data to be signed using token
    data = {
        'info': 'secret information',
    }

    token = create_access_token(data=data)
    return {'token': token}

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return False

# http://localhost:8080/note/20231204-212203/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjoic2VjcmV0IGluZm9ybWF0aW9uIiwiZXhwIjoxNzAxNzA3ODA1fQ.iDdApRxMPByLw_1OLspfmH9nm_mrSMBQrME3KY-FMOo