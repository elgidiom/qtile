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
~/.config/qtile/touchpad-setup.sh &


# Para bloquear la pantalla
~/.config/qtile/xidlehook.sh &

# redshift config

echo "Ejecutando autostart.sh" >> ~/.local/share/qtile/qtile.log


notify-send "Lanzando redshift"

(sleep 2 && redshift -c ~/.config/redshift/redshift.conf -l 8.742690:-75.884407) > ~/.redshift.log 2>&1 &
