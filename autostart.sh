#!/usr/bin/env sh

# Demonio de emacs
# emacs --daemon & lo dejé en el bashrc

# Gestor de transparencias
picom &

# Run Dropbox
flatpak run com.dropbox.Client &

# Run wifi
nm-applet &

# Configuración del teclado
setxkbmap -layout latam -option ctrl:swapcaps

# Demonio de notificaciones
dunst &

# Configuración del touch pad

## Activar el clic táctil
xinput set-prop "ELAN06FA:00 04F3:32BA Touchpad" "libinput Tapping Enabled" 1

## Configurar el desplazamiento vertical
xinput set-prop "ELAN06FA:00 04F3:32BA Touchpad" "libinput Natural Scrolling Enabled" 1
xinput set-prop "ELAN06FA:00 04F3:32BA Mouse" "libinput Natural Scrolling Enabled Default" 1

~/.config/qtile/xidlehook.sh
