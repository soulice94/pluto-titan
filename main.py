import asyncio
import strategies.strategy_1 as strategy1
import strategies.strategy_2 as strategy2

async def main():
    try:
        # result1 = await strategy1.run()
        result2 = await strategy2.run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
