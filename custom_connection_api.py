"""
This file provides an example robot for the Peerbots Platform's support for a custom robot.

First, the API must provide an endpoint describing the functionality desired by the robot.
Each function must provide an endpoiint at which this function can be accessed. 
"""

from peerbots_types import PeerbotsMessage

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the example API for a Peerbots custom robot connection"}

@app.get("/info")
def read_root():
    return {"data": {
        "name": "Custom Example",
        "endpoints": {
            "messages": "/message"
        },
        "configurations": [
            {
                "type": "joystick",
                "endpoint": "/move"
            },
            {
                "type": "joystick",
                "endpoint": "/head"
            },
            {
                "type": "button",
                "endpoint": "/click"
            },
            {
                "type": "slider",
                "endpoint": "/range",
                "minimum": 0,
                "maximum": 74,
                "step": 1
            }
        ]
    }}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}