from pydantic import BaseModel

class RomanSchema(BaseModel):
    link_bullet_points: list[str]

class ConversationShema(BaseModel):
    conversation_summary: str