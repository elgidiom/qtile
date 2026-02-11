# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# from qtile_extras import widget
# from qtile_extras.widget.decorations import RectDecoration

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os, subprocess

from libqtile.log_utils import logger


from libqtile import hook
from themes.palettes import get_theme, THEMES

"""Widget personalizados."""
from widgets.my_widget import ShutdownWidget

"""Funciones personalizadas."""
from functions.functions import task_name


@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


def space(len):
    return widget.Spacer(length=len)


 


mod = "mod4"
terminal = guess_terminal("kitty")
base_dir = "/home/gidiom/.config/qtile"

# --- Theme selection via .env/.env.local or environment ---
def _read_env_file(path: str):
    data = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    data[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return data

env_local = _read_env_file(os.path.join(base_dir, '.env.local'))
env_repo = _read_env_file(os.path.join(base_dir, '.env'))
theme_name = env_local.get('QTILE_THEME') or env_repo.get('QTILE_THEME') or os.environ.get('QTILE_THEME', 'ocean')
theme = get_theme(theme_name)

# Colors mapping used across the config
colors = {
    "background": theme.get("bar_bg", theme["bg"]),
    "foreground": theme["fg"],
    "highlight": theme["accent"],
    "decoration": theme.get("bg_alt", theme["bg"]),
}

# Theme string for rofi to override template colors at runtime
ROFI_THEME_STR = (
    f"* {{ fg0: {theme['fg']}; fg2: {theme.get('fg_muted', theme['fg'])}; "
    f"bg0: {theme['bg']}; bg2: {theme['accent']}; }}"
)

# Export for scripts (e.g., bluetooth.sh) launched from Qtile
os.environ["ROFI_THEME_STR"] = ROFI_THEME_STR

# paletas anteriores eliminadas en favor de themes/palettes.py

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])

# decor = {
#    "decorations": [
#        RectDecoration(colour=colors["decoration"],
#        radius=10,
#        filled=True,
#        padding_y=1,
#        group=True,
#        )
#     ]
# }

widget_top = [
    widget.Spacer(
        length=10,
    ),
    widget.Spacer(
        length=5,
    ),
    widget.QuickExit(
    default_text = '',
    countdown_format='{}',
    foreground = '525252',
    # fmt = '<b>{}</b>',
    countdown_start = 5,
    ),
    widget.TextBox(
        fmt='   ',
        foreground = '525252',
        mouse_callbacks = {'Button1': lazy.spawn(f"i3lock -i {base_dir}/wallpapers/lockscreen.jpg -F")}
    ),
    widget.Spacer(length=10),
    # Icono de volumen (solo visual; sin acciones para evitar conflictos)
    widget.PulseVolume(
        emoji=True,
        fmt='{}',
        emoji_list=['󰝟','','',''],
        step=5,
        # limit_max_volume=False,
        # mouse_callbacks={
        #     # Deshabilitar acciones por defecto con no-ops
        #     'Button1': lazy.spawn('true'),       # click izquierdo (mute)
        #     'Button4': lazy.spawn('true'),       # scroll arriba
        #     'Button5': lazy.spawn('true'),       # scroll abajo
        #     # Click derecho útil para abrir control
        #     'Button3': lazy.spawn('pavucontrol'),
        # },
    ),
    # Porcentaje de volumen (control principal: scroll/click)
    widget.PulseVolume(
        emoji=False,
        fmt='{}',
        step=5,
        limit_max_volume=False,
        # Click derecho abre pavucontrol (opcional)
        mouse_callbacks={'Button3': lazy.spawn('pavucontrol')},
    ),
    widget.Spacer(
        length=200,
    ),
    # widget.Spacer(),
    widget.GroupBox(
        active=colors["foreground"],
        highlight_method="block",
        this_current_screen_border="ffffff20",  # colors["highlight"],
        borderwidth=0,
        margin_x=0,
        padding_x=10,
        # background=colors["highlight"],
    ),
    widget.Spacer(),
    widget.Clock(
        format="<b>%a %d de %B  %H:%M:%S</b>",
        foreground=colors["foreground"],
        # mouse_callbacks={'Button1': lambda : subprocess.Popen(['./galendae/galendae'])},
        # fontsize=16,
        padding=10,
    ),
    widget.Spacer(),
    widget.Prompt(),
    widget.Pomodoro(
        color_active=colors["foreground"],
        # fontsize=16,
        color_inactive=colors["foreground"],
        # background='#ffffff50',
        padding=16,
        length_pomodori=25,
    ),
    # widget.Redshift(),
    widget.Spacer(
        length=100,
    ),
    # widget.Notify(
    #     # default_timeout_urgent=15,
    #     padding=20,
    #     # audiofile=base_dir + "/songs/notify.wav",
    #     scroll=True,
    #     width=320,
    #     parse_text=lambda x: x.replace("\n", ""),
    #     scroll_step=1,
    #     scroll_interval=0.006,
    #     scroll_fixed_width=True,
    #     scroll_delay=1,
    # ),
    # widget.Wlan(
    #     interface="wlp2s0",
    #     padding=15,
    #     # format='{essid} {percent:2.0%}'
    # ),
    # widget.Bluetooth(),
    widget.Memory(
        measure_mem="G",
        format="{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}",
    ),
    widget.Systray(),
    # space(10),
    widget.Spacer(
        length=5,
    ),
    #widget.Spacer( length=10),
    widget.Battery(
        foreground=colors["foreground"],
        format="{char} {percent:2.0%}",
        update_interval=10,
        show_short_text=False,
        notify_below=20,
        charge_char="",
        discharge_char="",
        full_char="",
        low_percentage=0.2,
    ),
]

# Mismo diseño de barra para monitor secundario (sin Systray para evitar conflicto).
widget_top_secondary = [
    widget.Spacer(
        length=10,
    ),
    widget.Spacer(
        length=5,
    ),
    widget.QuickExit(
    default_text = '',
    countdown_format='{}',
    foreground = '525252',
    countdown_start = 5,
    ),
    widget.TextBox(
        fmt='   ',
        foreground = '525252',
        mouse_callbacks = {'Button1': lazy.spawn(f"i3lock -i {base_dir}/wallpapers/lockscreen.jpg -F")}
    ),
    widget.Spacer(length=10),
    widget.PulseVolume(
        emoji=True,
        fmt='{}',
        emoji_list=['󰝟','','',''],
        step=5,
    ),
    widget.PulseVolume(
        emoji=False,
        fmt='{}',
        step=5,
        limit_max_volume=False,
        mouse_callbacks={'Button3': lazy.spawn('pavucontrol')},
    ),
    widget.Spacer(
        length=200,
    ),
    widget.GroupBox(
        active=colors["foreground"],
        highlight_method="block",
        this_current_screen_border="ffffff20",
        borderwidth=0,
        margin_x=0,
        padding_x=10,
    ),
    widget.Spacer(),
    widget.Clock(
        format="<b>%a %d de %B  %H:%M:%S</b>",
        foreground=colors["foreground"],
        padding=10,
    ),
    widget.Spacer(),
    widget.Prompt(),
    widget.Pomodoro(
        color_active=colors["foreground"],
        color_inactive=colors["foreground"],
        padding=16,
        length_pomodori=25,
    ),
    widget.Spacer(
        length=100,
    ),
    widget.Memory(
        measure_mem="G",
        format="{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}",
    ),
    widget.Spacer(
        length=5,
    ),
    widget.Battery(
        foreground=colors["foreground"],
        format="{char} {percent:2.0%}",
        update_interval=10,
        show_short_text=False,
        notify_below=20,
        charge_char="",
        discharge_char="",
        full_char="",
        low_percentage=0.2,
    ),
]

widget_bottom = [
    # space(5),
    # widget.GroupBox(
    #     active=colors["highlight"],
    #     highlight_method="block",
    #     this_current_screen_border="00000060",  # colors["highlight"],
    #     borderwidth=1,
    #     margin_x=5,
    #     padding_x=10,
    #     # background=colors["highlight"],
    # ),

    widget.Prompt(
        foreground=colors["foreground"],
        background=colors["background"],
    ),
    # widget.WindowName(
    #     # format = '{name}',
    #     foreground=colors["foreground"],
    # ),
    widget.Spacer(),
    widget.TaskList(
        parse_text=task_name,
        margin=0,
        icon_size=20,
        border="00000060",  # colors['background'],
        # borderwidth=4,
        highlight_method="block",
        padding_x=15,
    ),
    widget.Spacer(),
    # widget.Net(
    #     interface="wlp2s0",
    #     # format="{essid} {percent:2.0%}",
    #     foreground=colors["foreground"],
    # ),
    # widget.MemoryGraph(
    #     foreground=colors["foreground"],
    #     # background=colors["highlight"],
    #     graph_color=colors["highlight"],
    # ),
    widget.Memory(
        measure_mem="G",
        format="{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}",
    ),
    widget.Spacer(
        length=5,
    ),
    #widget.Spacer( length=10),
    widget.Battery(
        foreground=colors["foreground"],
        format="{char} {percent:2.0%}",
        update_interval=10,
        show_short_text=False,
        notify_below=20,
        charge_char="",
        discharge_char="",
        full_char="",
        low_percentage=0.2,
    ),
   # widget.Spacer(
   #     length=5,
   # ),
    widget.Spacer(
        length=5,
    ),
]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "period", lazy.next_screen(), desc="Focus next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Focus previous monitor"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "x", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui")),
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "e", lazy.spawn("nautilus -w")),
    # Intercambiando Control con Caps tecla
    # Key([], "Caps_Lock", lazy.function(lambda q: q.group.cmd_togroup("control"))),
    # Key([alt], "Tab", lazy.group.next_window(), desc="Focus next window"),
    # Key(["control"], "Caps_Lock", lazy.function(lambda q: q.group.cmd_togroup("control"))),
    # Configuración de teclas de sonido
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q sset Master toggle")),
    Key([], "XF86AudioPause", lazy.spawn("playerctl stop")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    # Configuración de brillo
    Key([], "XF86MonBrightnessDown", lazy.spawn(f"{base_dir}/brigthness.sh -d")),
    Key([], "XF86MonBrightnessUp", lazy.spawn(f"{base_dir}/brigthness.sh -u")),
    # Rofi conf

    # Bluetooth
    Key([mod], "s", lazy.spawn(f"{base_dir}/bluetooth.sh")),
    #pass
    Key([mod], "p", lazy.spawn("passmenu")),


    Key([mod], "r", lazy.spawn(
        "rofi -show drun -modi drun -show-icons "
        "-m -1 "
        "-config /home/gidiom/.config/qtile/rofi/drun.rasi "
        f"-theme-str '{ROFI_THEME_STR}'"
    )),
    Key(
        [mod], "0", minimize_all(), desc="Toggle hide/show all windows on current group"
    ),
    Key([mod], "f", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod, "control"], "e", lazy.spawn("emacsclient -c -a 'emacs'")),
    Key([mod,"shift"], "0", lazy.spawn(f"i3lock -i {base_dir}/wallpapers/lockscreen.jpg -F")),
    Key([mod], "d", lazy.spawn(
        "rofi -show window -show-icons "
        "-m -1 "
        "-config /home/gidiom/.config/qtile/rofi/window.rasi "
        f"-theme-str '{ROFI_THEME_STR}'"
    )),

]

groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(toggle=True),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 3,
    "margin": 5,
    "border_focus": colors["highlight"],
    "border_normal": "#00000000",  # colors["foreground"],
    # "border_focus_stack":pallette[4]
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**{"margin":0}),
    # layout.Floating(**layout_theme)
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Spiral()
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=15,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper=base_dir + "/wallpapers/wallpaper_beach.jpg",
        wallpaper_mode="stretch",
        # bottom=bar.Bar(
        #     widgets=widget_bottom,
        #     size=30,
        #     background=colors["background"],
        # ),
        top=bar.Bar(
            widget_top,
            size=25,
            background=colors["background"],
        ),
    ),
    Screen(
        wallpaper=base_dir + "/wallpapers/wallpaper_beach.jpg",
        wallpaper_mode="stretch",
        top=bar.Bar(
            widget_top_secondary,
            size=25,
            background=colors["background"],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors["background"],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        # Match(wm_class="galendae"),  # calendario
        Match(title="Meet - "),  # calendario popup
        # Match(wm_window_role="pop-up"),
    ],
    no_reposition_rules=[
        # Match(wm_class="galendae"), # Calendario pop-up
        Match(title="Meet - "),
    ],
)

def _apply_keyboard_layout():
    subprocess.run(["setxkbmap", "-layout", "latam", "-option", "ctrl:swapcaps"])

def _apply_touchpad_settings():
    subprocess.Popen([os.path.join(base_dir, "touchpad-setup.sh")])

def _set_external_144hz():
    """Set 144Hz on connected external outputs when that refresh is available."""
    try:
        xr = subprocess.run(
            ["xrandr", "--query"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return

    if xr.returncode != 0 or not xr.stdout:
        return

    lines = xr.stdout.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if " connected" not in line or line.startswith("Screen "):
            i += 1
            continue

        output = line.split()[0]
        # Keep internal laptop panel untouched.
        if output.startswith(("eDP", "LVDS", "DSI")):
            i += 1
            continue

        mode_144_available = False
        current_mode = None
        preferred_mode = None

        j = i + 1
        while j < len(lines) and lines[j].startswith("   "):
            mode_line = lines[j].strip()
            if not mode_line:
                j += 1
                continue

            parts = mode_line.split()
            if parts:
                mode = parts[0]
                flags = " ".join(parts[1:])
                if "*" in flags:
                    current_mode = mode
                if "+" in flags and preferred_mode is None:
                    preferred_mode = mode
                if "144.00" in flags or "143.98" in flags or "144.01" in flags:
                    mode_144_available = True
            j += 1

        if mode_144_available:
            target_mode = current_mode or preferred_mode
            cmd = ["xrandr", "--output", output]
            if target_mode:
                cmd.extend(["--mode", target_mode])
            cmd.extend(["--rate", "144"])
            subprocess.run(cmd, check=False)

        i = j

@hook.subscribe.startup_once
def set_keyboard_layout():
    _apply_keyboard_layout()

@hook.subscribe.resume
def restore_keyboard():
    _apply_keyboard_layout()

@hook.subscribe.startup_once
def set_touchpad_settings():
    _apply_touchpad_settings()
    _set_external_144hz()

@hook.subscribe.resume
def restore_touchpad_settings():
    _apply_touchpad_settings()

@hook.subscribe.screen_change
def set_external_refresh_on_screen_change(_event):
    _set_external_144hz()

@hook.subscribe.client_new
def new_client(client):
    logger.warning(client.name)
    wm_class = client.get_wm_class()
    client_name = client.name
    if wm_class and "galendae" in wm_class:
        client.set_position_floating(817, 32)

    if client_name and "Meet -" in client_name:
        client.floating = True
        client.place(1462, 808, 446, 232, 0, None)

    if wm_class and "gnome-calculator" in wm_class:
        client.floating = True
        client.place(758, 260, 392, 514)
    if wm_class and "simplescreenrecorder" in wm_class:
        client.floating = True
        client.place(487,672, 687,220)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3"
@lazy.function
def switch_theme(qtile):
    names = sorted(THEMES.keys())
    menu = "\n".join(names)
    cmd = [
        "rofi", "-dmenu", "-i", "-p", "Tema",
        "-config", f"{base_dir}/rofi/menu.rasi",
        "-theme-str", ROFI_THEME_STR,
    ]
    try:
        proc = subprocess.run(cmd, input=menu, text=True, capture_output=True)
        choice = proc.stdout.strip()
    except Exception:
        return
    if not choice or choice not in THEMES:
        return
    env_local_path = os.path.join(base_dir, ".env.local")
    lines = []
    try:
        with open(env_local_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    written = False
    for i, line in enumerate(lines):
        if line.strip().startswith("QTILE_THEME="):
            lines[i] = f"QTILE_THEME={choice}\n"
            written = True
            break
    if not written:
        lines.append(f"QTILE_THEME={choice}\n")
    with open(env_local_path, "w") as f:
        f.writelines(lines)
    qtile.reload_config()

# Bind after function is defined to avoid NameError on reload
keys.append(Key([mod], "t", switch_theme))
