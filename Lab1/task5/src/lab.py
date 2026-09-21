import asyncio


async def first():
    print("Первая: 1")
    await asyncio.sleep(1)
    print("Первая: 2")
    await asyncio.sleep(4)
    print("Первая: 3")


async def second():
    print("Вторая: 1")
    await asyncio.sleep(3)
    print("Вторая: 2")
    await asyncio.sleep(1)
    print("Вторая: 3")
    await asyncio.sleep(1)
    print("Вторая: 4")


async def main():
    await asyncio.gather(first(), second())


if __name__ == "__main__":
    asyncio.run(main())
