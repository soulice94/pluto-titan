from ollama import AsyncClient

class Filter:
    def __init__(self, text_content, prompt):
        self.text_content = text_content
        self.prompt = prompt

    async def refine(self):
        result = ''
        async for part in await AsyncClient().generate(
            model="deepseek-r1:14b",
            prompt=self.prompt + self.text_content,
            stream=True,
        ):
            result += part.response
            print(part.response, end='')
        return result
