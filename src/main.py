import json
from pydantic import BaseModel
import uvicorn
import os.path
from  os import path
from fastapi import FastAPI, HTTPException
import datetime
from model import NoteItem

app = FastAPI()
class Note(BaseModel):
    id: int
    text: str
class NoteID(BaseModel):
    noteID: int
class Token(BaseModel):
    tken: str


class NoteInfo(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime
Authorization = False
AuthorizationPath = ""

# AuthorizationToken = ""
# notes_dir = "notes"
# tokens_file = "tokens.txt"

def getAllNotes(token: Token):
    if (path.exists(f'{AuthorizationPath}')and Authorization == True):
        files = os.listdir(f"{AuthorizationPath}")
        # for file in files:
        #     print(os.path.splitext(os.path.basename(file))[0])

        return [os.path.splitext(os.path.basename(file))[0] for file in files]

def userAuthorization(token: str):
    global Authorization
    global AuthorizationPath
    Authorization = True
    AuthorizationPath = f"{token}"
    if(path.exists(f'{AuthorizationPath}')):
        # return False
        Authorization = True
    else:
        os.mkdir(f"{AuthorizationPath}")
        Authorization = True
        # return True
    # print(AuthorizationPath)

def create_note(id: int):
    global AuthorizationPath
    global Authorization
    dateNow = datetime.datetime.now()
    if (path.exists(f'{id}.txt') or Authorization == False):
        return False
    else:
        print(AuthorizationPath)
        file = open(f'{AuthorizationPath}/{id}.txt','w')
        # file.close()
        response = NoteItem(
            created_at=dateNow,
            updated_at=dateNow,
            text="",
            id=id
        )
        json.dump(response.json(), file)
        return True

def update_note(id: int, text: str):
    global AuthorizationPath
    global Authorization
    dateNow = datetime.datetime.now()
    if (path.exists(f'{AuthorizationPath}/{id}.txt') and Authorization == True):
        file = open(f'{AuthorizationPath}/{id}.txt', 'w')
        response = NoteItem(
            created_at=dateNow,
            updated_at=dateNow,
            text=text,
            id=id
        )
        json.dump(response.json(), file)
        file.write(text)
        file.close()
        return True
    else:
        return False
def read_note(id: int):
    global AuthorizationPath
    global Authorization
    if (path.exists(f'{AuthorizationPath}/{id}.txt') and Authorization == True):
        file = open(f'{AuthorizationPath}/{id}.txt', 'r')
        data = json.load(file)
        return json.loads(data)
    else:
        return {"ABC"}
        # return file.read()
def delete_note(id: int):
    global AuthorizationPath
    global Authorization
    if (path.exists(f'{AuthorizationPath}/{id}.txt') and Authorization == True):
        os.remove(f'{AuthorizationPath}/{id}.txt')
        return True
    else:
        return False


@app.get("/read_note")
async def read_notes(noteid: NoteID):
    print("sdjnvjdfnv")
    return read_note(noteid.noteID)

@app.post("/update_note")
async def ureate_notes(note: Note):
    update_note(note.id, note.text)
    return {"id": note.id, "text": note.text}

@app.post("/create_note")
async def create_notes(noteid: NoteID):
    if (create_note(noteid.noteID)==True):
        return {"id": noteid.noteID, "Result": "Succsess"}
    else:
        return {"id": noteid.noteID, "Result": "Fail"}

@app.post("/delete_note")
async def delete_notes(noteid: NoteID):
    delete_note(noteid.noteID)
    return {"id": noteid.noteID}

@app.post("/Authorization")
async def delete_notes(token: Token):
    userAuthorization(token.tken)
    return {"Result": "Succsess"}
    # else:
        # return {"Result": "Fail"}

@app.get("/getAllNotes")
async def getNotes(token: Token):
    # if (getAllNotes(token.tken) == True):
    return getAllNotes(token.tken)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
