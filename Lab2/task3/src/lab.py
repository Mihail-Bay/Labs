import asyncio
from time import perf_counter
from pathlib import Path
import requests
import aiohttp


def fetch_sync(url):
    start = perf_counter()
    try:
        with requests.get(url, timeout=15) as response:
            response.raise_for_status()
            response.content
            status = str(response.status_code)
    except requests.RequestException as error:
        status = type(error).__name__
    return url, status, perf_counter() - start


def run_sync(urls):
    start = perf_counter()
    results = []
    for url in urls:
        result = fetch_sync(url)
        results.append(result)
        print(result)
    return results, perf_counter() - start


async def fetch_async(session, url):
    start = perf_counter()
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            await response.read()
            status = str(response.status)
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        status = type(error).__name__
    return url, status, perf_counter() - start


async def run_async(urls):
    start = perf_counter()
    results = []
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(
            timeout=timeout, trust_env=True) as session:
        tasks = [fetch_async(session, url) for url in urls]
        # Получаем результаты по мере завершения запросов.
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            print(result)
    return results, perf_counter() - start


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    urls = (path / "txt/input.txt").read_text().splitlines()
    print("Последовательно: URL, статус, время в секундах")
    results, total = run_sync(urls)
    print(f"Общее время: {total:.3f} с")
    print("Асинхронно: URL, статус, время в секундах")
    results, total = asyncio.run(run_async(urls))
    print(f"Общее время: {total:.3f} с")
