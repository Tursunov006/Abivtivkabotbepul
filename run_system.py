import os
import asyncio
import uvicorn
from web_server import app
from bot import start_bot

async def run_all():
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    config = uvicorn.Config(app=app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config)

    # Web ilova va Botni bir vaqtda 24/7 yurgizish
    await asyncio.gather(
        server.serve(),
        start_bot()
    )

if __name__ == "__main__":
    asyncio.run(run_all())
