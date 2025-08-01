from ollama import AsyncClient
from executor import Executor
import asyncio
import strategies.strategy_1 as strategy1

async def main():
    try:
        result = await strategy1.run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
