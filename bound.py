import time
import asyncio 
import os


def sync_read_files(file_names):
    start_time = time.time()
    for file_name in file_names:
        with open(file_name, 'r') as f:
            content = f.read()
        time.sleep(0.1)
    end_time = time.time()
    return end_time-start_time 


async def async_read_files(file_names):
    start_time = time.time()

    async def read_file(file_name):
        def _read():
            with open(file_name, 'r') as f:
                return f.read()
        content = await asyncio.to_thread(_read)
        await asyncio.sleep(0.1)
        return content
    await asyncio.gather(*[read_file(file_name) for file_name in file_names])
    end_time = time.time()
    return end_time - start_time


file_names = [f"test_file_{i}.txt" for i in range(1000)]
for file_name in file_names:
    with open(file_name, 'w') as f:
        f.write('This is test file\n'*1000)

sync_time = sync_read_files(file_names)
print(f"Synchronous execution time: {sync_time:.4f} seconds")

async_time = asyncio.run(async_read_files(file_names))
print(f"Asynchronous execution time: {async_time:.4f} seconds")

for file_name in file_names:
    os.remove(file_name)