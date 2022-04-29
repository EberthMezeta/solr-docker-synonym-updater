import queue
import traceback

import unidecode
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.models import Response

from app.synonym_updater import Updater


update_queue = queue.Queue()
app = FastAPI(docs_url="/")

@app.post("/update")
async def add_synonym_to_queue(word_list:list):
    try:
        unnaccented_words = [unidecode.unidecode(word) for word in word_list]
        update_queue.put(unnaccented_words)
        return Response(status_code=201)
    except:
        print(traceback.format_exc())
        return []

updater = Updater(update_queue)
updater.setDaemon(True)
updater.start()


if __name__=="__main__":
    update_queue.put(["beneficiario","destinatario","ganador","receptor","titular","ganador","medallista"])
    uvicorn.run("main:app",host='localhost', port=8092, reload=True, debug=True)
