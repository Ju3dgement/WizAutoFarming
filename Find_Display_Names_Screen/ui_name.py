import asyncio

from wizwalker import WizWalker

async def main(walker):
  p1 = walker.get_new_clients()[0]
  print("Starting Root Window hook")
  await p1.hook_handler.activate_root_window_hook()
  print("Starting Render Context hook")
  await p1.hook_handler.activate_render_context_hook()
  print("Hooking done")
  input("Press Enter to continue")
  a = await p1.root_window.debug_print_ui_tree()
  await asyncio.sleep(1000)

# Error Handling
async def run():
  walker = WizWalker()

  try:
    await main(walker)
  except:
    import traceback

    traceback.print_exc()

  await walker.close()


# Start
if __name__ == "__main__":
    asyncio.run(run())