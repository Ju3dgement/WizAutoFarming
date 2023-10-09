import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter


async def tp(p,x,y,z):
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.25)

async def press_x_and_tp(p, x, y, z):
  #TP to specififc location & press X on keyboard
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.25)
  await p.send_key(Keycode.X, 0.25)
  await asyncio.sleep(1.25)
  await p.send_key(Keycode.X, 0.25)


async def start_combat(handler):
  #register combat, will continue when combat ends
    try:
        await handler.wait_for_combat()
    except:
        print("Error with start combat - restarting function")
        await start_combat(handler)

async def manage_coordinate(p):
  runs = 1
  while True:
    if p.title == "p1":
      print(f"Initilizing kango farm")
    await asyncio.sleep(6)
    x,y,z = 64060.69, 33074.53, 153.56 # Outside dungeon
    await press_x_and_tp(p, x, y, z)
    await p.wait_for_zone_change()
    await asyncio.sleep(4)

    print (f"Waited zone to change! {p.title}")

    x,y,z = 130.53, -10, -100
    await press_x_and_tp(p, x,y,z) # TP to boss
    print (f"successful port {p.title} ")

    await asyncio.sleep(3)
    handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.35)) 
    await start_combat(handler)
    print(f"{p.title} Combat ended")

    await asyncio.sleep(1.5)
    x,y,z = 45.51, -13.01, -100 #Gather health/mana wisps
    await tp(p, x,y,z)
    await asyncio.sleep(2)

    x,y,z = 25, -1834, 0 # leave dungeon
    await tp(p, x, y, z)
    await asyncio.sleep(3)
    if p.title == "p1":
      print (f"Runs: {runs}")
      runs += 1


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
        await asyncio.sleep(18)

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