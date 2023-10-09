# DO NOT SHARE CODE AROUND!!!!!
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import WizSprinter
from SlackFighter import *
  
async def checking_potion_needed(clients):
  for player in clients:
    await player.use_potion_if_needed(health_percent=20, mana_percent=15)

async def setup(client):
  print(f"[{client.title}] Activating Hooks")
  await client.activate_hooks()
  await client.mouse_handler.activate_mouseless()

async def start_combat(clients):
  try: 
    itterative = []
    for player in clients:
      itterative.append(SlackFighter(player))
    await asyncio.gather(*[player_wait.wait_for_combat() for player_wait in itterative])
  except:
    start_combat(clients)

async def main(sprinter):
  sprinter.get_new_clients()
  clients = sprinter.get_ordered_clients()
  p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
  for i, p in enumerate(clients, 1):
    p.title = "p" + str(i)

  await asyncio.gather(*[setup(p) for p in clients])
  runs = 0
  while True:
    print(f"Initilizing Stone Key (Jabberwock) / Number of runs: {runs}")
    await asyncio.sleep(3)
    await checking_potion_needed(clients)
    await asyncio.gather(*[player.teleport(XYZ(3281, 9706, 190)) for player in clients]) # Outside dungeon
    await asyncio.sleep(3)
    await asyncio.gather (*[player.send_key(Keycode.X, 0.15) for player in clients])
    await asyncio.gather (*[player.send_key(Keycode.X, 0.25) for player in clients])
    await asyncio.gather(*[player.wait_for_zone_change() for player in clients])
    await asyncio.sleep(3)
    print (f"Waited zone to change!")
    await asyncio.sleep(3)
    for player in clients:
      await player.tp_to_closest_mob()
      await asyncio.sleep(0.5)
    print (f"Starting first fight!")
    await asyncio.sleep(1)
    await start_combat(clients) # Start first fight
    print ("Finished Run")
    await asyncio.sleep(3)
    await asyncio.gather(*[player.teleport(XYZ(-76, -3159 , -26))for player in clients])
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