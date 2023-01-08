import asyncio
from threading import Thread, get_ident
import tkinter as tk

def log(msg: str):
    print(f"tid<{get_ident()}>: {msg}")

win = tk.Tk()
win.title("Python is cool!")
canvas = tk.Canvas(win, width=720, height=480)
canvas.pack()
log("Window initialized")

async def build_context_runner():
    loop = asyncio.get_running_loop()

    def build_context():
        log("Adding blue rect...")
        canvas.create_rectangle(50, 50, 100, 100, fill="blue", outline = "blue")

        def add_red_rect():
            log("Adding red rect...")
            canvas.create_rectangle(150, 50, 200, 100, fill="red", outline = "red")

        loop.call_later(3, add_red_rect)

    loop.call_soon_threadsafe(build_context)


async def event_handler_context_runner():
    loop = asyncio.get_running_loop()

    def on_click(event : tk.Event):
            log(f"Clicked at: {event.x}, {event.y}")

    win.bind("<Button-1>", lambda *args: loop.call_soon_threadsafe(on_click, *args))    


def create_thread_isolated_loop():    
    def start_bg_loop(loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    bg_loop = asyncio.new_event_loop()
    t = Thread(target=start_bg_loop, args=(bg_loop,), daemon=True)
    t.start()

    return bg_loop

asyncio.run_coroutine_threadsafe(event_handler_context_runner(), create_thread_isolated_loop())
asyncio.run_coroutine_threadsafe(build_context_runner(), create_thread_isolated_loop())

win.mainloop()
