import asyncio
import time
import wizwalker
from wizwalker import WizWalker, XYZ
from wizwalker.client import Client
from wizwalker.constants import Keycode
from wizwalker.errors import MemoryReadError


async def main(walker):
  client = walker.get_new_clients()[0]
  await client.activate_hooks()
  #await client.mouse_handler.activate_mouseless()
  while True:
    print(await client.body.position())
    time.sleep(1)
    
        

# Error Handling
async def run():
  walker = WizWalker()

  try:
    await main(walker)
  except:
    import traceback

    traceback.print_exc()

  await walker.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())


    