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

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from libqtile import bar, layout# widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os, subprocess

from libqtile.log_utils import logger


from libqtile import hook

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
base_dir = "/home/juanda/.config/qtile"

pallette2 = ["#F6F1EB", "#393E41", "#e94f3799", "#3F88C5", "#44BBA460", "#242424E6"]

pallette = ["#F6F1EB", "#393E41", "#3F88C5","#242424E6"]

pallette1 = [
    "#ff1493",
    "#dda0ad",
    "#ff1493",
    "#ffffff"
]

colors = {
    "background": pallette[1],
    "foreground": pallette[0],
    "highlight": pallette[2],
    "decoration": pallette[3]
}

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])

decor = {
   "decorations": [
       RectDecoration(colour=colors["decoration"],
       radius=10,
       filled=True,
       padding_y=1,
       group=True,
       )
    ]
}

widget_top = [
    widget.Spacer(
        length=10,
    ),
    widget.Spacer(**decor,
        length=5,
    ),
    widget.PulseVolume(**decor,
        emoji=True,
        fmt='{}',
        emoji_list=['󰝟','','',''],
    ),
    widget.PulseVolume(**decor,
        emoji=False,
        fmt='{}',
        check_mute_string='nada',
    ),
    widget.Spacer(**decor,
        length=5,
    ),
    widget.Spacer(),
    widget.Clock(**decor,
        format="<b>%a %d de %B  %H:%M:%S</b>",
        foreground=colors["foreground"],
        mouse_callbacks={'Button1': lambda : subprocess.Popen(['./galendae/galendae'])},
        # fontsize=16,
        padding=10,
    ),
    widget.Spacer(),
    widget.Pomodoro(**decor,
        color_active=colors["foreground"],
        # fontsize=16,
        color_inactive=colors["foreground"],
        # background='#ffffff50',
        padding=16,
        length_pomodori=25,
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
    widget.Systray(**decor
    ),
    space(10),
]

widget_bottom = [
    space(5),
    widget.GroupBox(**decor,
        active=colors["highlight"],
        highlight_method="block",
        this_current_screen_border="00000060",  # colors["highlight"],
        borderwidth=1,
        margin_x=5,
        padding_x=10,
        # background=colors["highlight"],
    ),

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
    widget.Memory(**decor,
        measure_mem="G",
        format="{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}",
    ),
    widget.Spacer(**decor,
        length=5,
    ),
    #widget.Spacer(**decor, length=10),
    widget.Battery(**decor,
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
   # widget.Spacer(**decor,
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
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "x", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([], "F8", lazy.spawn("flameshot gui")),
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


    Key([mod], "r", lazy.spawn("rofi -show drun -modi drun -show-icons")),
    Key(
        [mod], "d", minimize_all(), desc="Toggle hide/show all windows on current group"
    ),
    Key([mod], "f", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod, "control"], "e", lazy.spawn("emacsclient -c -a 'emacs'")),
    Key([mod], "0", lazy.spawn(f"i3lock -i {base_dir}/wallpapers/lockscreen.jpg -F")),
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
    "margin": 0,
    "border_focus": colors["highlight"],
    "border_normal": colors["decoration"],  # colors["foreground"],
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
        wallpaper=base_dir + "/wallpapers/wallpaper_house.jpg",
        wallpaper_mode="stretch",
        bottom=bar.Bar(
            widgets=widget_bottom,
            size=30,
            background=colors["background"],
        ),
        top=bar.Bar(
            widget_top,
            size=30,
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
