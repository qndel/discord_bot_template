import os
import pickle
import asyncio

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def isHost():
    return os.path.exists("./hostPC")
    
async def setBotVariable(b):
    global bot
    bot = b
################