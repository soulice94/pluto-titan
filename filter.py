from ollama import AsyncClient
import uuid

class Filter:
    def __init__(self, text_content, prompt):
        self.text_content = text_content
        self.prompt = prompt

    async def refine(self):
        result = ''
        uuid_str = str(uuid.uuid4())
        async for part in await AsyncClient().generate(
            model="deepseek-r1:14b",
            prompt=self.prompt + self.text_content,
            stream=True,
        ):
            result += part.response
            print(uuid_str, end=' ')
            print(part.response, end='')
        return result.split('</think>')[1].strip() if '</think>' in result else result.strip()
