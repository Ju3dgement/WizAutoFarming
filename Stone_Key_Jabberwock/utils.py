import asyncio
# from matplotlib.pyplot import spring

from wizwalker import XYZ
from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter.sprinty_client import MemoryReadError
#from sprinty_client import SprintyClient

potion_ui_buy = [
    "fillallpotions",
    "buyAction",
    "btnShopPotions",
    "centerButton",
    "fillonepotion",
    "buyAction",
    "exit"
]


async def is_control_grayed(button):
    return await button.read_value_from_offset(688, "bool")

async def get_window_from_path(root_window, name_path):
    async def _recurse_follow_path(window, path):
        if len(path) == 0:
            return window

        for child in await window.children():
            if await child.name() == path[0]:
                found_window = await _recurse_follow_path(child, path[1:])
                if not found_window is False:
                    return found_window

        return False

    return await _recurse_follow_path(root_window, name_path)

async def auto_buy_potions(client):
    # Head to home world gate
    await asyncio.sleep(0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.2)

    # Go to Wizard City
    leftButton = await get_window_from_path(
        client.root_window,
        ['WorldView','', 'messageBoxBG', 'ControlSprite', 'optionWindow', 'leftButton'])
    while not await is_control_grayed(leftButton):
        await client.mouse_handler.click_window(leftButton)
    await client.mouse_handler.click_window_with_name('wbtnWizardCity')
    await asyncio.sleep(0.15)
    await client.mouse_handler.click_window_with_name('teleportButton')
    await client.wait_for_zone_change()
    # Walk to potion vendor
    await client.goto(-0.5264079570770264, -3021.25244140625)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(11.836355209350586, -1816.455078125)
    await client.send_key(Keycode.W, 0.5)
    await client.wait_for_zone_change()
    await client.goto(-587.87927246093752, 404.43939208984375)
    await asyncio.sleep(1)
    await client.goto(-3965.254638671875, 1535.5472412109375)
    await asyncio.sleep(1)
    await client.goto(-4442.06005859375, 1001.5532836914062)
    await asyncio.sleep(1)
    while not await client.is_in_npc_range():
        await client.goto(-4442.06005859375, 1001.5532836914062)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1)
    # Buy potions
    while True:
        try:
            for i in potion_ui_buy:
                await client.mouse_handler.click_window_with_name(i)
                await asyncio.sleep(0.4)
        except ValueError:
            continue
        break
    # Return
    #await client.send_key(Keycode.PAGE_UP, 0.1)
    #await client.wait_for_zone_change()
    #await client.send_key(Keycode.PAGE_DOWN, 0.1)

async def get_text(client, text):
    name, *_ = await client.root_window.get_windows_with_name(f"{text}")
    text = (await name.maybe_text())
    return text

async def get_objective(p) -> str:
    obj = await get_text(p, "txtGoalName")
    obj = obj.split("in ", 1)[0]
    obj = obj.lower()
    obj = obj.split("<center>", 1)[1]
    return obj


async def go_through_dialog(client):
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)

async def safe_tp_to_mana(client):
  try:
    await client.tp_to_closest_mana_wisp()
  except MemoryReadError:
    await safe_tp_to_mana(client)
async def safe_tp_to_health(client):
  try:
    await client.tp_to_closest_health_wisp()
  except MemoryReadError:
    await safe_tp_to_health(client)

# async def decide_heal(client):
#     sprinty = SprintyClient(client)
#     if await sprinty.needs_potion(health_percent=15, mana_percent=15):
#         print(f'[{client.title}] Health is at {round((await sprinty.calc_health_ratio()* 100), 2)}% and mana is at {round((await sprinty.calc_mana_ratio() * 100), 2)}%. Need to recover.')
#         if await sprinty.has_potion():
#             await sprinty.use_potion()
            
#         elif await client.stats.current_gold() >= 15000 and await client.stats.reference_level() > 5: 
#             print(f"[{client.title}] Enough gold, buying potions")
#             await auto_buy_potions(client)
            

        
async def train_start(client):
    for entity in await client.get_base_entities_with_name("HOUSE_SP_TrainGauntlet_Teleporter"):
        train_loc = await entity.location()
    await client.teleport(train_loc)
    await asyncio.sleep(1.25)
    if not await client.is_in_npc_range():
        try:
            await client.goto(train_loc.x, train_loc.y)
        except ZeroDivisionError:
            pass
    while not await client.is_in_npc_range():
        continue
    await client.send_key(Keycode.X, 0.1)
    await client.wait_for_zone_change()
        
async def teleport_to_npc(client, npc_str: str):
    for entity in await client.get_base_entities_with_name(npc_str):
        npc = await entity.location()
    await client.teleport(npc)
    while not await client.is_in_npc_range():
        pass

async def set_active(client) -> str:
    while (quest_root := await get_window_from_path(
        client.root_window,
        ["WorldView", "DeckConfiguration","wndQuestList"
         ]
        )) == False:
            await client.send_key(Keycode.Q, 0.1)
            await asyncio.sleep(1)
    for i in range(4):
        try:
            dungeon_icon = await get_window_from_path(
                quest_root,
                [f"wndQuestInfo{i}","questInfoWindow","wndQuestInfo","imgEncounter",
                 ]
                )
        except AttributeError:
            await client.send_key(Keycode.Q, 0.1)
            return print("No more quests...")
        if await dungeon_icon.is_visible():
            await client.mouse_handler.click_window_with_name(f"wndQuestInfo{i}")
            await asyncio.sleep(1)
            await client.send_key(Keycode.Q, 0.1)
            
            return print("Found active gauntlet")
        
    await client.send_key(Keycode.Q, 0.1)
    return print("Couldn't find active quest's world!")



