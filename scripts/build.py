from PyInstaller.__main__ import run as pyi

pyi(
    [
        "--onefile",
        "--windowed",
        "--name",
        "PowerDesktop",
        "power_desktop/__main__.py",
    ]
)
