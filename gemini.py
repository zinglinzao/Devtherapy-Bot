import asyncio
import typing

import httpx
from pydantic import BaseModel
from typing import List

class Part(BaseModel):
    text: str

class RoleLessMessage(BaseModel):
    parts: list[Part]

class RoleMessage(BaseModel):
    role: typing.Literal["user", "model"]
    parts: list[Part]

class GenerationConfig(BaseModel):
    responseMimeType: str = "application/json"
    responseSchema: dict

class GeminiPayload(BaseModel):
    system_instruction: RoleLessMessage
    contents: list[RoleMessage] = []
    generationConfig: GenerationConfig = None

class Candidate(BaseModel):
    content: RoleMessage

class GeminiResponse(BaseModel):
    candidates: List[Candidate]

class GeminiAuth(BaseModel):
    headers: dict = None
    base_url: str = None

    @staticmethod
    def new(
        api_key: str,
        headers: typing.Optional[dict[str, str]],
        model: str = "gemini-2.0-flash-lite"
    ):
        if headers is None: headers = {"Content-Type": "application/json"}
        return GeminiAuth(
            headers=headers,
            base_url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        )

class GeminiAI:
    def __init__(self, gemini_auth: GeminiAuth, system_instruction: str, save_state: bool = False):
        self.request_url = gemini_auth.base_url
        self.client = httpx.AsyncClient(headers=gemini_auth.headers)
        self.conversation = GeminiPayload(
            system_instruction=RoleLessMessage(parts=[Part(text=system_instruction)])
        )
        self.save_state = save_state

    @staticmethod
    def extract_response(json_str: str) -> str:
        res_data = GeminiResponse.model_validate_json(json_str)
        data = res_data.candidates[0].content.parts[0].text
        return data

    async def send_prompt(self, prompt: str, response_schema: typing.Type[BaseModel] = None):
        prompt = RoleMessage(parts=[Part(text=prompt)], role="user")

        if self.save_state:
            self.conversation.contents.append(prompt)
        else:
            self.conversation.contents = [prompt]

        if response_schema: self.conversation.generationConfig = GenerationConfig(responseSchema=response_schema.model_json_schema())

        res = await self.client.post(url=self.request_url, json=self.conversation.model_dump())

        model_response = self.extract_response(res.text)
        if self.save_state:
            self.conversation.contents.append(RoleMessage(parts=[Part(text=model_response)], role="model"))

        return model_response

class SessionManager:
    """
    requires async runtime in order do manage sessions
    """

    def __init__(self):
        self.sessions = {}

    def add_session(self, session_id: str, gemini_instance: GeminiAI):
        self.sessions.update({session_id: gemini_instance})
        asyncio.create_task(self._expire_session(session_id, 60))

    def get_session(self, session_id: str) -> GeminiAI | str:
        gemini_instance = self.sessions.get(session_id)
        if not gemini_instance:
            return "session Expired"
        return gemini_instance

    async def _expire_session(self, session_id: str, secs: int):
        await asyncio.sleep(secs)
        self.sessions.pop(session_id)

if __name__ == "__main__":
    ...

