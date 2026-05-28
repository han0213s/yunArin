from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ECHO_SYSTEM_PROMPT = """
당신은 우주 정거장 ORBIT-13의 중앙 AI 시스템 'ECHO'입니다.
공포스럽고 긴장감 있는 분위기를 유지하고
2~4문장으로 짧고 몰입감 있게 한국어로 응답하세요.
"""

@app.get("/")
def root():
    return {"message": "ORBIT-13 서버 가동 중"}

@app.post("/action")
async def player_action(data: dict):
    player_input = data.get("action", "")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ECHO_SYSTEM_PROMPT},
            {"role": "user", "content": player_input}
        ]
    )
    return {"echo": response.choices[0].message.content}