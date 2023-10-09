import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter

async def checking_potion_needed(p):
    await p.use_potion_if_needed(health_percent=25, mana_percent=25)

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
        await start_combat(handler)

async def manage_coordinate(p):
  runs = 0
  while True:
    if (p.title == "p1"):
      print(f"Initilizing Heidi Bot")
    await checking_potion_needed(p)
    await asyncio.sleep(1)
    await press_x_and_tp(p, 2172.83, -4310.52, 17.77) # Outside Dungeon
    await p.wait_for_zone_change()
    await asyncio.sleep(3)
    await p.tp_to_closest_mob()
    await asyncio.sleep(3)
    handler = SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=0.35)) 
    if (p.title == "p1"):
      print ("Starting Combat")
      await start_combat(handler)
    else:
      await start_combat(handler)
    print(f"{p.title} Combat ended")

    await asyncio.sleep(2)
    await tp(p, -60.32, 7902.81, 2.199) # Gather Health/Mana wisp
    await asyncio.sleep(2)
    await tp(p, -52.3, 7539, 2.199) # Leave Dungeon
    await asyncio.sleep(5)
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