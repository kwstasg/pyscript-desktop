from js import document
from pyodide.ffi import create_proxy

def show_window(window_id):
    window = document.getElementById(window_id)
    window.style.display = "block"

def hide_window(window_id):
    window = document.getElementById(window_id)
    window.style.display = "none"

def minimize_window(event):
    event.target.closest('.window').style.display = "none"

def maximize_window(event):
    window = event.target.closest('.window')
    if window.style.width == "100vw":
        window.style.width = "500px"
        window.style.height = "400px"
        window.style.top = "50px"
        window.style.left = "50px"
    else:
        window.style.width = "100vw"
        window.style.height = "100vh"
        window.style.top = "0"
        window.style.left = "0"

def make_draggable(window_id):
    window = document.getElementById(window_id)
    titlebar = window.querySelector(".titlebar")
    offsetX = offsetY = 0

    def drag_start(event):
        nonlocal offsetX, offsetY
        offsetX = event.clientX - window.offsetLeft
        offsetY = event.clientY - window.offsetTop
        document.addEventListener("mousemove", drag_proxy)
        document.addEventListener("mouseup", drag_end_proxy)

    def drag(event):
        window.style.left = f"{event.clientX - offsetX}px"
        window.style.top = f"{event.clientY - offsetY}px"

    def drag_end(event):
        document.removeEventListener("mousemove", drag_proxy)
        document.removeEventListener("mouseup", drag_end_proxy)

    drag_start_proxy = create_proxy(drag_start)
    drag_proxy = create_proxy(drag)
    drag_end_proxy = create_proxy(drag_end)

    titlebar.addEventListener("mousedown", drag_start_proxy)

# Show windows on icon click
document.getElementById("icon1").addEventListener("click", create_proxy(lambda event: show_window("window1")))
document.getElementById("icon2").addEventListener("click", create_proxy(lambda event: show_window("window2")))

# Window control buttons
document.getElementById("close1").addEventListener("click", create_proxy(lambda event: hide_window("window1")))
document.getElementById("close2").addEventListener("click", create_proxy(lambda event: hide_window("window2")))

document.getElementById("minimize1").addEventListener("click", create_proxy(minimize_window))
document.getElementById("minimize2").addEventListener("click", create_proxy(minimize_window))

document.getElementById("maximize1").addEventListener("click", create_proxy(maximize_window))
document.getElementById("maximize2").addEventListener("click", create_proxy(maximize_window))

# Make windows draggable
make_draggable("window1")
make_draggable("window2")
