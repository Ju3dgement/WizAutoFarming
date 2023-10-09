# DO NOT SHARE CODE AROUND!!!!!
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import WizSprinter
from WizFighter import *
from functools import partial
from wizwalker import utils
#from SlackFighter import *
from SlackFighter import *


async def crown_item_seed(p):
  try:
    await p.mouse_handler.click_window_with_name("centerButton")
    return True
  except:
    return False

async def gray_out(p):
  try:
    await p.mouse_handler.click_window_with_name("SellButton")
    return True
  except:
    await asyncio.sleep(1)
    await click_window_named(p, "exit")
    return False

async def click_window_named(p, button_name):
  """Mouse handler for clickable items on screen"""
  window = partial(p.mouse_handler.click_window_with_name, button_name)
  await utils.wait_for_non_error(window)

async def quicksell(p):
  await p.send_key(Keycode.U, 0.1)
  await asyncio.sleep(1)
  await click_window_named(p, "QuickSell_Item")
  await asyncio.sleep(1)
  await click_window_named(p, "ShopCategory_Seed")
  await asyncio.sleep(1)
  await click_window_named(p, "AllAction")
  await asyncio.sleep(1)
  flag = await crown_item_seed(p)
  if flag:
    print("Sold all crown seeds")
  else:
    print ("sold all seeds")
  await asyncio.sleep(1)
  await click_window_named(p, "sellAction")
  flag2 = await gray_out(p)
  await asyncio.sleep(2)
  await p.send_key(Keycode.U, 0.1)
  #await click_window_named(p, "SellButton")
  
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
  selling_counter = 0
  while True:
    print(f"Initilizing Synthonium Farm / Number of runs: {runs}")
    await asyncio.sleep(3)
    await checking_potion_needed(clients)
    await asyncio.gather(*[player.teleport(XYZ(7774, 6431, -1463)) for player in clients]) # Outside dungeon
    await asyncio.sleep(3)
    await asyncio.gather (*[player.send_key(Keycode.X, 0.15) for player in clients])
    await asyncio.gather (*[player.send_key(Keycode.X, 0.25) for player in clients])
    await asyncio.gather(*[player.wait_for_zone_change() for player in clients])
    await asyncio.sleep(3)
    print (f"Waited zone to change!")
    await dialogue(clients)
    await asyncio.sleep(3)
    for player in clients:
      await player.tp_to_closest_mob()
      await asyncio.sleep(0.5)
    #await asyncio.gather(*[player.teleport(XYZ(102.3, 906.3, 2.1)) for player in clients])
    print (f"Starting first fight!")
    await asyncio.sleep(1)
    await start_combat(clients) # Start first fight
    print ("Starting second fight!")
    await asyncio.gather(*[player.teleport(XYZ(-20, 4977, 2.1))for player in clients])
    await start_combat(clients) # Start second fight
    print ("Finished Run")
    await asyncio.gather(*[player.teleport(XYZ(-4, 6.1 ,2.19))for player in clients])
    await asyncio.sleep(6)
    await asyncio.gather(*[player.send_key(Keycode.ENTER, 0.2) for player in clients])
    await asyncio.sleep(5)
    runs += 1
    # selling_counter += 1
    # if selling_counter == 1:
    #   await asyncio.gather(*[quicksell(p) for p in clients])
    #   selling_counter = 0
      

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