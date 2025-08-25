from ollama import AsyncClient


class Filter:
    def __init__(self, text_content, prompt):
        self.text_content = text_content
        self.prompt = prompt

    async def refine(self):
        result = ""
        async for part in await AsyncClient().generate(
            model="gpt-oss:20b",
            prompt=self.prompt + self.text_content,
            stream=True,
        ):
            result += part.response
            # print(part.response, end='')
        print(f"Filter result: {result}")
        # need to transform the string result into an array
        return (
            result.split("</think>")[1].strip().split("\n")
            if "</think>" in result
            else result.strip().split("\n")
        )
