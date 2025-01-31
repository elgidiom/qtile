#!/usr/bin/env sh

# Demonio de emacs
# emacs --daemon & lo dejé en el bashrc

# Demonio de notificaciones
dunst &

# Gestor de transparencias
picom &
notify-send "Picom lanzado"

# Run Dropbox
flatpak run com.dropbox.Client &
notify-send "Dropbox corriendo"

# Run wifi
nm-applet &

# Configuración del teclado
setxkbmap -layout latam -option ctrl:swapcaps

# Configuración del touch pad

## Activar el clic táctil
xinput set-prop "ELAN06FA:00 04F3:32BA Touchpad" "libinput Tapping Enabled" 1

## Configurar el desplazamiento vertical
xinput set-prop "ELAN06FA:00 04F3:32BA Touchpad" "libinput Natural Scrolling Enabled" 1
xinput set-prop "ELAN06FA:00 04F3:32BA Mouse" "libinput Natural Scrolling Enabled Default" 1

# Para bloquear la pantalla
~/.config/qtile/xidlehook.sh &

# redshift config

echo "Ejecutando autostart.sh" >> ~/.local/share/qtile/qtile.log


notify-send "Lanzando redshift"

(sleep 2 && redshift -c ~/.config/redshift/redshift.conf -l 8.742690:-75.884407) > ~/.redshift.log 2>&1 &
