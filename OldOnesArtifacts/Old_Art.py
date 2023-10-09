#DO NOT SHARE CODE AROUND!!!!!
import asyncio
from wizwalker.constants import Keycode
from wizwalker.utils import XYZ
from wizwalker.extensions.wizsprinter import WizSprinter
from functools import partial
from wizwalker import utils

async def press_x_and_tp(p, x, y, z):
  """Used to collect on ground items"""
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(1)
  await p.send_key(Keycode.X, 0.1)
  await asyncio.sleep(1)

async def tp_and_move(p, x, y, z):
  """Used to swap between areas"""
  await p.teleport(XYZ(x, y, z))
  await asyncio.sleep(6)  

async def click_window_named(p, button_name):
  """Mouse handler for clickable items on screen"""
  window = partial(p.mouse_handler.click_window_with_name, button_name)
  await utils.wait_for_non_error(window)

async def switch_realm(p, current_realm, realm_number, realm_number_counter):
  """Function for cycling each realm / starts page 2 (Diego) ends page 5 (Wraith) will loop back after ending"""
  print (f"Attempting to switch to realm {current_realm}")
  await asyncio.sleep(2)
  await p.send_key(Keycode.ESC, 0.1)
  await asyncio.sleep(0.5)
  await click_window_named(p, "RealmsTab")
  #print ("Successfully clicked realm button")
  await asyncio.sleep(1)
  for i in range(realm_number_counter + 1):
    await click_window_named(p,"btnRealmRight")
    await asyncio.sleep(0.5)
  #print ("Successfully clicked right realm button")
  await asyncio.sleep(1)
  await click_window_named(p,"btnRealm" + f"{realm_number}")
  await asyncio.sleep(1)
  print(f"Successfully swapped to realm {current_realm} on {p.title}")
  await click_window_named(p, "btnGoToRealm")
  await asyncio.sleep(7)

async def ursai_village_coordinates(p, wooden_chest):
  """Find collectable entities in the night forest excluding chests"""
  print(f"Location: Ursai Village @ {p.title}")

  x,y,z = -4568, -2644, 393.1 # Location 1 OOA Ursai
  await press_x_and_tp(p, x, y, z)

  x,y,z = 986.4, -5744, 225 # location 2 OOA Ursai
  await press_x_and_tp(p, x, y, z)

  x,y,z = 2270, -2859, 249 # location 3 OOA Ursai
  await press_x_and_tp(p, x, y, z)

  x,y,z = -8317, -2743, 370 # location 4 OOA Ursai
  await press_x_and_tp(p, x, y, z)

  x,y,z = 13.40, -948.29, 48.9 # location 5 OOA Ursai
  await press_x_and_tp(p, x, y, z)

  x,y,z = -3864, -3724, 316 # location 6 OOA Ursai
  await press_x_and_tp(p, x, y, z)

  if wooden_chest:
    x,y,z = 1932.45, -5347.47, 336.14 # location 1 Chest ursai_village
    await press_x_and_tp(p, x, y, z)

    x,y,z = -5400.69, -1195.97, 335.34 # location 2 Chest ursai_village
    await press_x_and_tp(p, x, y, z)

    x,y,z = -2644.14, -810.36, 66.60 # location 3 Chest ursai_village
    await press_x_and_tp(p, x, y, z)

    x,y,z = -3000.66, -3784.39, 327.12 # location 4 Chest ursai_village
    await press_x_and_tp(p, x, y, z)

async def wildlands_coordinates(p, wooden_chest):
  """Find collectable entities in the wildlands"""
  print(f"Location: Wildlands @ {p.title}")
  x,y,z = 2310, 5234, 358.8 # Location 1 OOA WildLands
  await press_x_and_tp(p, x, y, z)

  x,y,z = -1691.9, 3615.3, 156.4 # Location 2 OOA WildLands
  await press_x_and_tp(p, x, y, z)

  x,y,z = 420.9, 1837.5, 150.6 # Location 3 OOA WildLands
  await press_x_and_tp(p, x, y, z)

  x,y,z = -8018.6, 4249, 332.6 # Location 4 OOA WildLands
  await press_x_and_tp(p, x, y, z)

  x,y,z = 2671.6, 2399.3, 147.5 # Location 5 OOA WildLands
  await press_x_and_tp(p, x, y, z)

  x,y,z = 7344.40, -5541.65, 382.77 # Location 6 OOA WildLands
  await press_x_and_tp(p, x, y, z)

  if wooden_chest:
    x,y,z = -5659.9, -1662, 120 # Location 1 Chest WildLands
    await press_x_and_tp(p, x, y, z)

    x,y,z = 5885.8, -6688, 378.6 # Location 2 Chest WildLands
    await press_x_and_tp(p, x, y, z)

    x,y,z = 5549.8, 13510, 516.9 # Location 3 Chest WildLands
    await press_x_and_tp(p, x, y, z)

async def night_forest_coordinates(p, wooden_chest):
  """Find collectable entities in the night forest"""
  print(f"Location: Night Forest @ {p.title}")

  x,y,z = 11384.1, -329.5, -339.7 # Location 1 OOA The Night Forest
  await press_x_and_tp(p, x, y, z)

  x,y,z = -4454.56201171875, 5543.1513671875, 242.71658325195312 # Location 2 OOA The Night Forest
  await press_x_and_tp(p, x, y, z)

  if wooden_chest:
    x,y,z = -4286.2, -4198, -319.9 # Location 1 Chest The Night Forest
    await press_x_and_tp(p, x, y, z)

    x,y,z = 2578, 4717.9, -34.5 # Location 2 Chest The Night Forest
    await press_x_and_tp(p, x, y, z)

    x,y,z = -1891.1, 4880.8, -26 # Location 3 Chest The Night Forest
    await press_x_and_tp(p, x, y, z)

    x,y,z = -3964.93, 4668.81, 242.71 # Location 4 Chest The Night Forest
    await press_x_and_tp(p, x, y, z)

async def badlands_coordinates(p, wooden_chest):
  """Find collectable entities in the badlands"""
  print (f"Location: Badlands @ {p.title}")

  x,y,z = 15998.72, -354.60, 262.17 # Location 1 OOA Badlands
  await press_x_and_tp(p, x, y, z)

  x,y,z = -460.12, -2002.63, 1.38 # Location 2 OOA Badlands
  await press_x_and_tp(p, x, y, z)

  x,y,z = 11997.54, -13121, 22.63 # Locxxation 3 OOA Badlands
  await press_x_and_tp(p, x, y, z)

  x,y,z = 3909.52, -11808.27, -5.76 # Location 4 OOA Badlands
  await press_x_and_tp(p, x, y, z)
  await asyncio.sleep(2)

  if wooden_chest:
    x,y,z = 8546.16, -11048.18, 22.30 # Location 1 Chest Badlands
    await press_x_and_tp(p, x, y, z)

    x,y,z = 13643.69, -5441.41, 5.41 # Location 2 Chest Badlands
    await press_x_and_tp(p, x, y, z)
  
async def find_position_realm(realms, player_realm):
  for i, x in enumerate(realms):
    if player_realm in x:
      return (i, x.index(player_realm))

async def manage_coordinate(p, wooden_chest, player1_realm, player2_realm, player3_realm, player4_realm):
  """Main function"""
  amount_of_runs = 1
  realms = [["Diego", "Drake", "Dryad", "Dworgyn", "Falmea", "Ghoul", "Greyrose"],
  ["Helephant", "Humongofrog", "Imp", "Ivan", "Kelvin", "Kraken", "Leprechaun"],
  ["Lincoln", "Orthrus", "Phoenix", "Pixie", "Satyr", "Scarecrow", "Seraph"],
  ["Stormzilla", "Sunbird", "Torrence", "Troll", "Unicorn", "Vampire", "Wraith"]]
  realm_number = [0, 1, 2, 3, 4, 5, 6]
  realm_page_number = [0, 1, 2, 3]
  if (p.title == "p1"):
    realm_number_counter, realm_counter = await find_position_realm(realms, player1_realm.title())
  elif (p.title == "p2"):
    realm_number_counter, realm_counter = await find_position_realm(realms, player2_realm.title())
  elif (p.title == "p3"):
    realm_number_counter, realm_counter = await find_position_realm(realms, player3_realm.title())
  else:
    realm_number_counter, realm_counter = await find_position_realm(realms, player4_realm.title())

  #realm_counter = 0
  # realm_number_counter = 0
  print("==============================================================")
  print ("To whomever manage to get a copy of this code intentionally or from the owner / friend")
  print ("DO NOT SHARE CODE AROUND!!!")
  print ("The less people who knows, the better\n")
  print("If you want to exit this program, press 'ctrl + c' on the current prompt")
  print("READ 'Configs.txt' FOR ALL INSTRUCTIONS")
  if wooden_chest:
    print("Wooden chest has been activated!")
  else:
    print("Wooden chest has been deactivated!")
  await asyncio.sleep(3)
  print("==============================================================")

  while True:
    print(f"Initilizing <Old One's Artifact> farm @ {p.title}")
    await switch_realm(p, realms[realm_number_counter][realm_counter], realm_number[realm_counter], realm_page_number[realm_number_counter])

    await ursai_village_coordinates(p, wooden_chest)

    x,y,z = -423, 2925.8, 120.2 # Ursai Village -> The WildLands
    await tp_and_move(p, x, y, z)

    await wildlands_coordinates(p, wooden_chest)

    x,y,z = -5637.3, 17664, 282.5 # WildLands -> The Night Forest
    await tp_and_move(p, x, y, z)

    await night_forest_coordinates(p, wooden_chest)

    x,y,z = 8060.11, -3578.75, -741.10 # The Night Forest -> Badlands
    await tp_and_move(p, x, y, z)

    await badlands_coordinates(p, wooden_chest)

    x,y,z = 7264.74, 1207.71, 4.45 # Badlands -> The Night Forest
    await tp_and_move(p, x, y, z)

    x,y,z = -6558.8, -4857.2, -243.6 # The Night Forest -> The WildLands
    await tp_and_move(p, x, y, z)

    x,y,z = -7981.1, 3588.6, 282.7 # The WildLands -> Ursai Village
    await tp_and_move(p, x, y, z)

    #Realm manager for itteration
    if realm_page_number[realm_number_counter] == 3 and realm_number[realm_counter] == 6: 
      realm_number_counter = 0
      realm_counter = 0
    elif realm_number[realm_counter] == 6: 
      realm_counter = 0
      realm_number_counter += 1 
    else:
      realm_counter += 1
    print("==============================================================")
    print(f"Number of run(s): {amount_of_runs} @ {p.title}")
    print("==============================================================")

    amount_of_runs += 1
    await asyncio.sleep(3)

async def main(sprinter):
  """Sub-Main function"""
  # Register clients
  sprinter.get_new_clients()
  clients = sprinter.get_ordered_clients()
  #p1 = [*clients, None][:1]
  p1, p2, p3, p4 = [*clients, None, None, None, None][:4]

  for i, p in enumerate(clients, 1):
    p.title = "p" + str(i)

  # Hook activation
  for p in clients: 
    print(f"[{p.title}] Activating Hooks")
    await p.activate_hooks()
    await p.mouse_handler.activate_mouseless()

  # Read Text File
  with open("Configs.txt", "r") as file:
    line_one = file.readline().replace("Wooden_Chest = ", "").strip()
    if (line_one == "True"):
      wooden_chest = bool(line_one)
    else: 
      wooden_chest = False

    player_A_Realm = file.readline().replace("player1_realm = ", "").strip()
    player_B_Realm = file.readline().replace("player2_realm = ", "").strip()
    player_C_Realm = file.readline().replace("player3_realm = ", "").strip()
    player_D_Realm = file.readline().replace("player4_realm = ", "").strip()

  # Create handlder for coordinates
  task = []
  for p in clients:
    task.append(asyncio.create_task(manage_coordinate(p, wooden_chest, player_A_Realm, player_B_Realm, player_C_Realm, player_D_Realm)))
  while True:
    await asyncio.sleep(10)

async def run():
  """Error Handling for wizsprinter"""
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
#DO NOT SHARE CODE AROUND!!!!!
