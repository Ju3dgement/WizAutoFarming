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
    entity_list = await client.get_base_entity_list()

    # for e in entity_list:
    #   try:
    #     object_template = await e.object_template()
    #     display_name_code = await object_template.display_name()
    #     display_name = await client.cache_handler.get_langcode_name(display_name_code)
    #     print(display_name)
    #   except:
    #     pass
    for e in entity_list:
      try:
        object_template = await e.object_template()
        display_name_code = await object_template.display_name()
        display_name = await client.cache_handler.get_langcode_name(display_name_code)
        print(display_name)
      except:
        pass

    time.sleep(100)
    
        

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


    