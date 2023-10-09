import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter


async def tp(p,x,y,z):
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1.25)
  await p.send_key(Keycode.W, 0.1)


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
  runs = 0
  while True:
    if (p.title == "p1"):
      print(f"Initilizing Jade Oni Bot")
    await asyncio.sleep(1)
    x,y,z = -1997, 121.81, 100 # @ obleisk spawn
    await press_x_and_tp(p, x, y, z)
    await asyncio.sleep(3)
    
    x,y,z = -5520, 29/81, 767
    await press_x_and_tp(p, x,y,z)

    await asyncio.sleep(3)
    handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.35)) 
    if (p.title == "p1"):
      await start_combat(handler)
    else:
      await asyncio.sleep(6)
      await start_combat(handler)


    print(f"{p.title} Combat ended")

    await asyncio.sleep(1.5)
    x,y,z = -5520, 29/81, 767 #Gather health/mana wisps
    await tp(p, x,y,z)
    await asyncio.sleep(3)
    runs += 1
    if (p.title == "p1"):
      print ("==============================")
      print ("Combat ended")
      print(f"Number of runs: {runs}")
      print ("==============================")



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