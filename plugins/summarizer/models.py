from pydantic import BaseModel

class ConversationShema(BaseModel):
    conversation_summary: str
