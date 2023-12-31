import asyncio

from wizwalker.constants import Keycode
from wizwalker.extensions.wizsprinter.sprinty_client import MemoryReadError


potion_ui_buy = [
    "fillallpotions",
    "buyAction",
    "btnShopPotions",
    "centerButton",
    "fillonepotion",
    "buyAction",
    "exit"
]


async def logout_and_in(client):
    await client.send_key(Keycode.ESC, 0.1)
    await asyncio.sleep(0.4)
    await client.mouse_handler.click_window_with_name('QuitButton')
    await asyncio.sleep(0.4)
    if await client.root_window.get_windows_with_name('centerButton'):
        await asyncio.sleep(0.4)
        await client.mouse_handler.click_window_with_name('centerButton')
    await asyncio.sleep(7)
    await client.mouse_handler.click_window_with_name('btnPlay')
    await client.wait_for_zone_change()

async def go_through_dialog(client):
    while not await client.is_in_dialog():
        await asyncio.sleep(0.1)
    while await client.is_in_dialog():
        await client.send_key(Keycode.SPACEBAR, 0.1)

async def auto_buy_potions(client):
    # Head to home world gate
    await asyncio.sleep(0.1)
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(1.2)
    # Go to Wizard City
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
    await client.goto(-880.2447509765625, 747.2051391601562)
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
    await client.send_key(Keycode.PAGE_UP, 0.1)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.1)

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

async def collect_wisps(client):
    # Head to home world gate
    await client.send_key(Keycode.HOME, 0.1)
    await client.wait_for_zone_change()
    while not await client.is_in_npc_range():
        await client.send_key(Keycode.S, 0.1)
    await client.send_key(Keycode.X, 0.1)
    await asyncio.sleep(0.5)
    # Go to Mirage
    for i in range(3):
        await client.mouse_handler.click_window_with_name('rightButton')
    await asyncio.sleep(0.1)
    await client.mouse_handler.click_window_with_name('wbtnMirage')
    await asyncio.sleep(0.1)
    await client.mouse_handler.click_window_with_name('teleportButton')
    await client.wait_for_zone_change()
    # Collecting wisps
    while await client.stats.current_hitpoints() < await client.stats.max_hitpoints():
        await safe_tp_to_health(client)
        await asyncio.sleep(0.4)
    while await client.stats.current_mana() < await client.stats.max_mana():
        await safe_tp_to_mana(client)
        await asyncio.sleep(0.4)
    # Return
    await client.send_key(Keycode.PAGE_UP, 0.2)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.2)

async def low_collect_wisps(client):
    # Head to start of world
    await asyncio.sleep(0.1)
    await client.send_key(Keycode.END, 0.1)
    # Recover
    while await client.stats.current_hitpoints() < await client.stats.max_hitpoints():
        await safe_tp_to_health(client)
        await asyncio.sleep(0.4)
    while await client.stats.current_mana() < await client.stats.max_mana():
        await safe_tp_to_mana(client)
        await asyncio.sleep(0.4)
    # Return
    await client.send_key(Keycode.PAGE_UP, 0.1)
    await client.wait_for_zone_change()
    await client.send_key(Keycode.PAGE_DOWN, 0.2)
    

async def finished_combat(client):
    await asyncio.sleep(0.1)
    position = await client.body.position()
    while position.y >= -743.0302734375:
        try:
            await client.goto(11040.29296875, -732.3465576171875)
        except ZeroDivisionError:
            break
        position = await client.body.position()
    await asyncio.sleep(2)
    return

        
        
        
    


async def decide_heal(client):
    if await client.needs_potion(health_percent=10, mana_percent=21):
        print(f'[{client.title}] Health is at {round((await client.calc_health_ratio()* 100), 2)}% and mana is at {round((await client.calc_mana_ratio() * 100), 2)}%. Need to recover.')
        if await client.has_potion():
            await client.use_potion()
            
        elif await client.stats.current_gold() >= 15000 and await client.stats.reference_level() > 5: 
            print(f"[{client.title}] Enough gold, buying potions")
            await auto_buy_potions(client)
            
        elif await client.stats.reference_level() >= 110:
            print(f"[{client.title}] Low gold, collecting wisps")
            await collect_wisps(client)
        else:
            print(f"[{client.title}] Collecting wisps")
            await low_collect_wisps(client)
