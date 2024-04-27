#!/usr/bin/env python3
from libqtile.widget import base

class ShutdownWidget(base._TextBox):
    def __init__(self, text="⏻", fontsize=10, **config):
        super().__init__(text, **config)
        self.add_defaults({"font": "Arial",
                         #   "padding": 3,
                           })
        self.fontsize = fontsize  # Tamaño predeterminado si no se especifica
        self.button_press = [self.shutdown]

    def shutdown(self, qtile):
        import subprocess
        subprocess.Popen(["shutdown", "-h", "now"])
