# DO NOT SHARE CODE AROUND!!!!!
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import WizSprinter
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter import SprintyCombat, CombatConfigProvider, WizSprinter
from wizwalker import XYZ
from wizwalker.constants import Keycode

async def checking_potion_needed(clients):
  for player in clients:
    await player.use_potion_if_needed(health_percent=20, mana_percent=15)

async def setup(client):
  print(f"[{client.title}] Activating Hooks")
  await client.activate_hooks()
  await client.mouse_handler.activate_mouseless()

async def start_combat(clients):
  itterative = []
  for p in clients:
    itterative.append(SprintyCombat(p, CombatConfigProvider(f'configs/{p.title}spellconfig.txt', cast_time=.3)))
    await asyncio.sleep(2)
  await asyncio.gather(*[player_wait.wait_for_combat() for player_wait in itterative])

async def main(sprinter):
  sprinter.get_new_clients()
  clients = sprinter.get_ordered_clients()
  p1, p2, p3, p4 = [*clients, None, None, None, None][:4]
  for i, p in enumerate(clients, 1):
    p.title = "p" + str(i)

  await asyncio.gather(*[setup(p) for p in clients])
  runs = 0
  while True:
    print(f"Initilizing Heidi bot / Number of runs: {runs}")
    await checking_potion_needed(clients)
    await asyncio.sleep(3)
    await asyncio.gather(*[player.teleport(XYZ(2401.56, -4395, 17)) for player in clients]) # Outside dungeon
    await asyncio.sleep(3)
    await asyncio.gather (*[player.send_key(Keycode.X, 0.2) for player in clients])
    await asyncio.gather (*[player.send_key(Keycode.X, 0.2) for player in clients])
    await asyncio.gather(*[player.wait_for_zone_change() for player in clients])
    print (f"Waited zone to change!")
    await asyncio.sleep(3)
    for players in clients:
      await players.tp_to_closest_mob()
      await players.send_key(Keycode.W, 0.1)
      await asyncio.sleep(1)
    # await asyncio.gather(*[player.teleport(XYZ(-52.3, 7539, 2.199)) for player in clients]) # teleport to heidi 
    await start_combat(clients)
    await asyncio.sleep(2)
    await asyncio.gather(*[player.teleport(XYZ(581.17, 6450.39, 2.199))for player in clients])
    await asyncio.sleep(6)
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