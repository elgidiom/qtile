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
~/.config/qtile/keyboard-reapply.sh &

# Configuración del touch pad

# Detectar automáticamente el nombre del touchpad (más seguro que usar id)
DEVICE=$(xinput list | grep -i 'touchpad' | awk -F'\t' '{print $2}' | sed 's/^↳ //')

if [ -n "$DEVICE" ]; then
    # Activar tap-to-click
    xinput set-prop "$DEVICE" "libinput Tapping Enabled" 1
    # Activar scroll natural
    xinput set-prop "$DEVICE" "libinput Natural Scrolling Enabled" 1
else
    echo "No se detectó touchpad."
fi


# Para bloquear la pantalla
~/.config/qtile/xidlehook.sh &

# redshift config

echo "Ejecutando autostart.sh" >> ~/.local/share/qtile/qtile.log


notify-send "Lanzando redshift"

(sleep 2 && redshift -c ~/.config/redshift/redshift.conf -l 8.742690:-75.884407) > ~/.redshift.log 2>&1 &
