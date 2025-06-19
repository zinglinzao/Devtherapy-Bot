from discord import Message

# it recommended to put Config initialization here but not necessary. this function will execute first
async def on_ready():
    ...

# this is just example. function name determines on which discord event function will react
# check py-cord docs for  more details
async def on_message(msg: Message):
    ...
