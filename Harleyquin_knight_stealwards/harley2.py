# DO NOT SHARE CODE AROUND!!!!!
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import WizSprinter
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
#from SlackFighter import *
from WizFighter import *
  
async def checking_potion_needed(player):
    await player.use_potion_if_needed(health_percent=20, mana_percent=15)

async def setup(client):
  print(f"[{client.title}] Activating Hooks")
  await client.activate_hooks()
  await client.mouse_handler.activate_mouseless()

async def start_combat(player):
  try: 
    list_list = []
    list_list.append(HighLevelCombat(player))
    await player.wait_for_combat()
  except:
    await start_combat(player)

async def start_combat2(player):
  await asyncio.sleep(5)
  SprintyCombat(player, CombatConfigProvider(f'configs/{player.title}spellconfig.txt', cast_time=0.4))
  await player.wait_for_combat()

async def start_combat3(handler):
  #register combat, will continue when combat ends
  try:
    await handler.wait_for_combat()
  except:
    print("Error with start combat - restarting function")
    await start_combat(handler)

async def manage_coordinate(player):
  runs = 0
  while True:
    if player.title == "p1":
        print(f"Initilizing Harley Quinn / Number of runs: {runs}")
    await asyncio.sleep(3)
    await checking_potion_needed(player)
    await player.teleport(XYZ(-37, 13154, 4.5)) # Outside dungeon
    await asyncio.sleep(3)
    await player.send_key(Keycode.X, 0.15)
    await player.send_key(Keycode.X, 0.25)
    await player.wait_for_zone_change()
    await asyncio.sleep(3)
    if player.title == "p1":
        print (f"Waited zone to change!")
    await asyncio.sleep(3)
    await player.tp_to_closest_mob()
    if player.title == "p1":
        print (f"Starting first fight!")
    handler = SprintyCombat(player, CombatConfigProvider(f'configs/{player.title}spellconfig.txt', cast_time=.3))
    await asyncio.sleep(2)
    await start_combat3(handler) # Start first fight
    await player.teleport(XYZ(-27, 57, 0)) # Gather health/mana
    if player.title == "p1":
        print ("Finished Run")
    await asyncio.sleep(3)
    await player.teleport(XYZ(16.8, -1508, 0)) # Leave dungeon

    await asyncio.sleep(5)
    if player.title == "p1":
        runs += 1
async def main(sprinter):
  sprinter.get_new_clients()
  clients = sprinter.get_ordered_clients()
  p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
  for i, p in enumerate(clients, 1):
    p.title = "p" + str(i) 
  await asyncio.gather(*[setup(p) for p in clients])
  task = []
  for p in clients:
    task.append(asyncio.create_task(manage_coordinate(p)))
  while True:
    await asyncio.sleep(10)
    

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