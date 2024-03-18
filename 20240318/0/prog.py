import asyncio

async def echo(reader, writer):
    while data := await reader.readline():
        line = data.split()
        if line[0] == 'print':
            writer.write(' '.join(line[1:]))
        writer.write(data.swapcase())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())