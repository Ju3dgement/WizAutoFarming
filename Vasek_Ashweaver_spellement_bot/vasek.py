import asyncio
from time import time

from wizwalker.constants import Keycode
from wizwalker.utils import XYZ, wait_for_non_error
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from functools import partial
from wizwalker import utils

async def tp(p,x,y,z):
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.25)

async def press_x_and_tp(p, x, y, z):
  #TP to specififc location & press X on keyboard
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.25)
  await p.send_key(Keycode.X, 0.25)
  await asyncio.sleep(1.25)
  await p.send_key(Keycode.X, 0.25)#Double check if hotkey was not pressed first time


async def start_combat(handler):
  #register combat, will continue when combat ends
    try:
        await handler.wait_for_combat()
    except:
        print("Error with start combat - restarting function")
        await start_combat(handler)

async def manage_coordinate(p):
  while True:
    print(f"Initilizing Vasek Bot {p.title}")
    await asyncio.sleep(3)
    x,y,z = 8186.42, -6858.04, -916.79 # Outside dungeon
    await press_x_and_tp(p, x, y, z)
    await p.wait_for_zone_change()
    print (f"Waited zone to change! {p.title}")

    x,y,z = 0.32, 572.95, 0.0# Go to boss
    await tp(p, x,y,z)
    print (f"successful port {p.title} to boss")

    await asyncio.sleep(5)
    handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.35)) 
    await start_combat(handler)
    print(f"{p} Combat ended")

    await asyncio.sleep(1)
    x,y,z = -2.570, -17.15, -3.051 #Gather health/mana wisps
    await tp(p, x,y,z)
    await asyncio.sleep(2)

    x,y,z = -4.07, 1783.314, 0.00 # leave dungeon
    await tp(p, x, y, z)
    await asyncio.sleep(3)

async def main(sprinter):
    # Register clients
    sprinter.get_new_clients()
    clients = sprinter.get_ordered_clients()
    p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
    for i, p in enumerate(clients, 1):
        p.title = "p" + str(i)

    # Hook activation
    for p in clients: 
        print(f"[{p.title}] Activating Hooks")
        await p.activate_hooks()
        await p.mouse_handler.activate_mouseless()


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


# Start
if __name__ == "__main__":
    asyncio.run(run())