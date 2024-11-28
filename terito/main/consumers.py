import aiohttp
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EssayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Parse form data from the WebSocket message
        data = json.loads(text_data)

        # Construct the prompt dynamically
        prompt = (
            f"Write a {data.get('tone', 'professional')} essay for a university application. "
            f"The applicant's name is {data.get('name')}, they are {data.get('age')} years old, "
            f"currently living in {data.get('location')}. Their best subject is {data.get('best_subject')}, "
            f"and they find {data.get('worst_subject')} challenging."
        )

        # Stream the essay content from Ollama
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "phi3.5", "prompt": prompt},
                ) as response:
                    if response.status == 200:
                        # Read the response stream and send updates to the client
                        async for chunk in response.content.iter_any():
                            await self.send(text_data=json.dumps({"message": chunk.decode()}))
                    else:
                        error_message = await response.text()
                        await self.send(text_data=json.dumps({"error": f"Error: {error_message}"}))
        except Exception as e:
            await self.send(text_data=json.dumps({"error": f"Exception: {str(e)}"}))
