import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ, wait_for_non_error
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter

async def tp(p,x,y,z):
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.25)

async def press_x_and_tp(p, x, y, z):
  #TP to specififc location & press X on keyboard
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.5)
  await p.send_key(Keycode.X, 0.25)


async def start_combat(handler):
  #register combat, will continue when combat ends
  try:
    await handler.wait_for_combat()
  except:
    print("Error with start combat - restarting function")
    await start_combat(handler)

async def manage_coordinate(p):
  runs = 0
  while True:
    print(f"Initilizing Zarathonyx Bot {p.title}")
    await asyncio.sleep(3)
    x,y,z = 16567.42, -14580.22, 933.84 # Outside dungeon
    await press_x_and_tp(p, x, y, z)
    await p.wait_for_zone_change()
    print (f"Waited zone to change! {p.title}")
    await asyncio.sleep(2)
    x,y,z = -218, 531, 0.12
    await press_x_and_tp(p, x,y,z)
    await asyncio.sleep(5)
    handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.4)) 
    await start_combat(handler)
    await asyncio.sleep(2)
    x,y,z = 19.761241912841797, -8.791147232055664, 0.123504638671875 #Gather health/mana wisps
    await tp(p, x,y,z)
    await asyncio.sleep(2)

    x,y,z = 16.40, 1357.314, 0.12 # leave dungeon
    await tp(p, x, y, z)

    if (p.title == "p1"):
      runs += 1
      print (f"Number of runs: {runs}")
    await asyncio.sleep(2)

async def main(sprinter):
  # Register clients
  sprinter.get_new_clients()
  clients = sprinter.get_ordered_clients()
  p1, p2 = [*clients, None, None][:2]
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
