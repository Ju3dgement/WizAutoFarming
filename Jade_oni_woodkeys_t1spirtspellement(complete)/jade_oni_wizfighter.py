# DO NOT SHARE CODE AROUND!!!!!
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import WizSprinter
from WizFighter import *

async def checking_potion_needed(clients):
  for player in clients:
    await player.use_potion_if_needed(health_percent=20, mana_percent=15)

async def setup(client):
  print(f"[{client.title}] Activating Hooks")
  await client.activate_hooks()
  await client.mouse_handler.activate_mouseless()

async def start_combat(clients):
  itterative = []
  for player in clients:
    itterative.append(HighLevelCombat(player))
  await asyncio.gather(*[player_wait.wait_for_combat() for player_wait in itterative])

async def dialogue(clients):
  player = []
  for player in clients:
    while not await player.is_in_dialog():
      await asyncio.sleep(0.1)
    while await player.is_in_dialog():
      await player.send_key(Keycode.SPACEBAR, 0.1)
  await asyncio.sleep(2)

async def main(sprinter):
  sprinter.get_new_clients()
  clients = sprinter.get_ordered_clients()
  p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
  for i, p in enumerate(clients, 1):
    p.title = "p" + str(i)

  await asyncio.gather(*[setup(p) for p in clients])
  runs = 0
  while True:
    print(f"Initilizing Jade oni / Number of runs: {runs}")
    await checking_potion_needed(clients)
    await asyncio.sleep(3)
    await asyncio.gather(*[player.teleport(XYZ(-1997, 121.81, 100)) for player in clients]) # obblisk
    await asyncio.sleep(3)
    await asyncio.gather (*[player.send_key(Keycode.X, 0.15) for player in clients])
    await asyncio.gather (*[player.send_key(Keycode.X, 0.25) for player in clients])
    await asyncio.sleep(3)
    await asyncio.gather(*[player.teleport(XYZ(-5520, 29/81, 767)) for player in clients])
    print (f"Jade Oni Fight!")
    await start_combat(clients)
    await asyncio.gather(*[player.teleport(XYZ(-5520, 29/81, 767))for player in clients]) # health & mana wisp
    await asyncio.sleep(5)
    runs += 1

async def run():
  sprinter = WizSprinter() 
  try:
    await main(sprinter)
  except:
    import traceback
    traceback.print_exc()
  await sprinter.close()

if __name__ == "__main__":
    asyncio.run(run())
# DO NOT SHARE CODE AROUND!!!!!