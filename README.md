
# Desktop Environment in PyScript

This project creates a web-based desktop environment using PyScript. Users can launch and interact with various web applications in draggable, resizable windows.

## Features

- **Draggable and Resizable Windows**
- **Window Controls**: Minimize, maximize, and close buttons.
- **Application Icons**: Clickable icons to open applications.
- **Embedded Iframes**: Applications are opened in iframes within the windows.

## Setup and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/pyscript-desktop.git
   cd pyscript-desktop
   ```

2. **Start the Server**:
   - **Option 1**: Using Python's HTTP server:
     ```bash
     python3 -m http.server
     ```
     Open your browser and navigate to `http://localhost:8000`.
   
   - **Option 2**: Using Live Server in VS Code:
     - Install the Live Server extension in VS Code.
     - Right-click `index.html` and select `Open with Live Server`.

## Adding Applications

To add new applications, modify the `apps` list in `python/main.py`:

```python
# Add Apps Here
apps = [
    {"id": 1, "name": "Paint", "icon": "fas fa-paint-roller", "src": "https://jspaint.app/"},
    {"id": 2, "name": "Diablo", "icon": "fas fa-gamepad", "src": "https://d07riv.github.io/diabloweb/"},
    {"id": 3, "name": "Visual Studio Code", "icon": "fas fa-code", "src": "https://emupedia.net/emupedia-app-vscode/"},
    {"id": 4, "name": "Python Console", "icon": "fa-brands fa-python", "src": "https://pyodide.org/en/stable/console.html"},
    # Add more apps here
]
```

### Attributes of `apps`

Each application in the `apps` list is represented by a dictionary with the following keys:

- `id` (int): A unique identifier for the application.
- `name` (str): The display name of the application.
- `icon` (str): The FontAwesome class for the application's icon.
- `src` (str): The URL to be loaded in an iframe when the application is opened.


## File Structure

```
pyscript-desktop/
├── css/
│   └── styles.css
├── plugins/
│   └── fontawesome/
│   └── pyscript/
├── python/
│   └── main.py
├── .gitignore
├── index.html
└── README.md
```
