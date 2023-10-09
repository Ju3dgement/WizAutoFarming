#DO NOT SHARE
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from wizwalker.constants import Keycode
from WizFighter import *
from utils import go_through_dialog, decide_heal
from wizwalker.extensions.scripting.utils import teleport_to_friend_from_list

async def start_combat(clients):
  itterative = []
  for p in clients:
    itterative.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=.3)))
  await asyncio.gather(*[player_wait.wait_for_combat() for player_wait in itterative])

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
  runs = 0
  while True:
    print(f"Initilizing Synth Bot / Number of Runs: {runs}")
    start_zone = await p1.zone_name()
    await asyncio.sleep(1)
    await asyncio.gather(*[p.use_potion_if_needed(health_percent=65, mana_percent=25) for p in clients])
    await p1.teleport(XYZ(7764, 6532, -1463.89)) # Outside dungeon
    await asyncio.sleep(1)
    await p1.send_key(Keycode.X, 0.1)
    await p1.send_key(Keycode.X, 0.2)
    await p1.wait_for_zone_change()
    next_zone = await p1.zone_name()
    await asyncio.sleep(1.4)
    print ("Waited zone to change!")
    await asyncio.gather(*[p.send_key(Keycode.F, 0.2) for p in clients[1:]])
    await asyncio.gather(*[teleport_to_friend_from_list(p, icon_list=2, icon_index=0) for p in clients[1:]]) #Fish Icon in friends list
    await asyncio.gather(*[p.wait_for_zone_change(start_zone) for p in clients[1:]])
    print("successful zone change")
    await asyncio.sleep(1)
    await asyncio.gather(*[go_through_dialog(player) for player in clients])
    for player in clients:
        await player.tp_to_closest_mob()
        await player.send_key(Keycode.W, 0.1)
        await asyncio.sleep(.5)
    print (f"successful port")
    await start_combat(clients)
    await asyncio.gather(*[go_through_dialog(player) for player in clients])
    await asyncio.gather(*[p.send_key(Keycode.W, 2) for p in clients])
    await asyncio.sleep(5)
    for player in clients:
        await player.tp_to_closest_mob()
        await player.send_key(Keycode.W, 0.1)
        await asyncio.sleep(0.1)
    print (f"successful port")
    await start_combat(clients)
    await asyncio.sleep(2)
    await p1.teleport(XYZ(-0.2, -0.2918, 2.199)) # Leave Dungeon
    await asyncio.sleep(1.5)
    await p1.mouse_handler.click_window_with_name('centerButton')
    await p1.wait_for_zone_change(next_zone)
    runs += 1

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