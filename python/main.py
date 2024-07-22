from js import document, window
from pyodide.ffi import create_proxy

# Add Apps Here
apps = [
    {"id": 1, "name": "Paint", "icon": "fas fa-paint-roller", "src": "https://jspaint.app/"},
    {"id": 2, "name": "Visual Studio Code", "icon": "fas fa-code", "src": "https://emupedia.net/emupedia-app-vscode/"},
    {"id": 3, "name": "Diablo", "icon": "fas fa-gamepad", "src": "https://d07riv.github.io/diabloweb/"}
]

# Function to generate the app's HTML structure
def generate_app_html(app):
    desktop = document.getElementById('desktop')

    # Create icon
    icon_div = document.createElement('div')
    icon_div.className = 'icon'
    icon_div.id = f'icon{app["id"]}'
    icon_i = document.createElement('i')
    icon_i.className = app['icon']
    icon_span = document.createElement('span')
    icon_span.textContent = app['name']
    icon_div.appendChild(icon_i)
    icon_div.appendChild(icon_span)
    desktop.appendChild(icon_div)

    # Create window
    window_div = document.createElement('div')
    window_div.className = 'window'
    window_div.id = f'window{app["id"]}'
    window_div.dataset.maximized = "false"

    titlebar_div = document.createElement('div')
    titlebar_div.className = 'titlebar'
    titlebar_div.textContent = app['name']

    buttons_div = document.createElement('div')
    buttons_div.className = 'buttons'

    minimize_span = document.createElement('span')
    minimize_span.id = f'minimize{app["id"]}'
    minimize_i = document.createElement('i')
    minimize_i.className = 'fas fa-window-minimize'
    minimize_span.appendChild(minimize_i)

    maximize_span = document.createElement('span')
    maximize_span.id = f'maximize{app["id"]}'
    maximize_i = document.createElement('i')
    maximize_i.className = 'fas fa-window-maximize'
    maximize_span.appendChild(maximize_i)

    close_span = document.createElement('span')
    close_span.id = f'close{app["id"]}'
    close_i = document.createElement('i')
    close_i.className = 'fas fa-times'
    close_span.appendChild(close_i)

    buttons_div.appendChild(minimize_span)
    buttons_div.appendChild(maximize_span)
    buttons_div.appendChild(close_span)

    titlebar_div.appendChild(buttons_div)
    window_div.appendChild(titlebar_div)

    content_div = document.createElement('div')
    content_div.className = 'content'
    content_div.style.position = 'relative'
    content_div.dataset.src = app['src']

    window_div.appendChild(content_div)
    desktop.appendChild(window_div)

# Function to open the app link in a new tab
def open_link(app):
    content_div = document.querySelector(f'#window{app["id"]} .content')
    content_div.innerHTML = ""
    link = document.createElement('a')
    link.href = app['src']
    link.target = '_blank'
    link.textContent = f"Open {app['name']} in a new tab"
    content_div.appendChild(link)

for app in apps:
    generate_app_html(app)

# Function to bring a window to the front
def bring_to_front(window):
    windows = document.querySelectorAll('.window')
    for w in windows:
        w.style.zIndex = '0'
    window.style.zIndex = '10'

# Function to show the window
def show_window(window_id):
    window = document.getElementById(window_id)
    content_div = window.querySelector('.content')
    if not content_div.querySelector('iframe'):
        iframe = document.createElement('iframe')
        iframe.src = content_div.dataset.src
        iframe.style.width = "100%"
        iframe.style.height = "100%"
        iframe.style.border = "none"
        iframe.onerror = create_proxy(lambda event: open_link(app))
        content_div.appendChild(iframe)
    window.style.display = "block"
    bring_to_front(window)

# Function to hide the window
def hide_window(window_id):
    window = document.getElementById(window_id)
    content_div = window.querySelector('.content')
    iframe = content_div.querySelector('iframe')
    if iframe:
        content_div.removeChild(iframe)
    window.style.display = "none"

# Function to minimize the window
def minimize_window(event):
    event.target.closest('.window').style.display = "none"

# Function to maximize the window
def maximize_window(event):
    window = event.target.closest('.window')
    if window.dataset.maximized == "true":
        window.style.width = window.dataset.originalWidth
        window.style.height = window.dataset.originalHeight
        window.style.top = window.dataset.originalTop
        window.style.left = window.dataset.originalLeft
        window.dataset.maximized = "false"
    else:
        window.dataset.originalWidth = window.style.width
        window.dataset.originalHeight = window.style.height
        window.dataset.originalTop = window.style.top
        window.dataset.originalLeft = window.style.left
        window.style.width = "100vw"
        window.style.height = "100vh"
        window.style.top = "0"
        window.style.left = "0"
        window.dataset.maximized = "true"

# Function to make the window draggable
def make_draggable(window_id):
    window = document.getElementById(window_id)
    titlebar = window.querySelector(".titlebar")
    offsetX = offsetY = 0
    isDragging = False

    def drag_start(event):
        nonlocal offsetX, offsetY, isDragging
        offsetX = event.clientX - window.offsetLeft
        offsetY = event.clientY - window.offsetTop
        isDragging = True
        document.addEventListener("mousemove", drag_proxy, {"passive": True})
        document.addEventListener("mouseup", drag_end_proxy, {"passive": True})

    def drag(event):
        if isDragging:
            window.style.left = f"{event.clientX - offsetX}px"
            window.style.top = f"{event.clientY - offsetY}px"

    def drag_end(event):
        nonlocal isDragging
        isDragging = False
        document.removeEventListener("mousemove", drag_proxy)
        document.removeEventListener("mouseup", drag_end_proxy)

    drag_start_proxy = create_proxy(drag_start)
    drag_proxy = create_proxy(drag)
    drag_end_proxy = create_proxy(drag_end)

    titlebar.addEventListener("mousedown", drag_start_proxy, {"passive": True})

# Function to initialize the desktop
def init_desktop():
    icons = document.querySelectorAll(".icon")
    for i, icon in enumerate(icons, start=1):
        window_id = f"window{i}"
        minimize_id = f"minimize{i}"
        maximize_id = f"maximize{i}"
        close_id = f"close{i}"
        
        # Show window on icon click
        icon.addEventListener("click", create_proxy(lambda event, window_id=window_id: show_window(window_id)), {"passive": True})

        # Window control buttons
        document.getElementById(close_id).addEventListener("click", create_proxy(lambda event, window_id=window_id: hide_window(window_id)), {"passive": True})
        document.getElementById(minimize_id).addEventListener("click", create_proxy(minimize_window), {"passive": True})
        document.getElementById(maximize_id).addEventListener("click", create_proxy(maximize_window), {"passive": True})

        # Make windows draggable
        make_draggable(window_id)

        # Bring to front on window mousedown
        document.getElementById(window_id).addEventListener("mousedown", create_proxy(lambda event, window_id=window_id: bring_to_front(document.getElementById(window_id))), {"passive": True})

init_desktop()
