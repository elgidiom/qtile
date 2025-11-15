#!/usr/bin/env sh

select=$(bluetoothctl devices | awk '{print $3,$4}' | rofi -dmenu -i -config /home/gidiom/.config/qtile/rofi/menu.rasi -theme-str "${ROFI_THEME_STR}")
MAC=$(bluetoothctl devices | grep "$select" | awk '{print $2}')
[ -z  "$MAC" ] && MAC=NoDeviceFound

connect=$(bluetoothctl info "$MAC" | grep Connected: | awk '{print $2}')
if [ "$connect" = no ]; then
    notify-send "Intentando conectarse a $select ."
    bluetoothctl connect "$MAC" && notify-send -u low "Conectado."|| notify-send "Conexión fallida." -u critical
elif [ "$connect" = yes ]; then
    notify-send "Intentando desconectarse de $select ."
    bluetoothctl disconnect "$MAC" && notify-send "Desconectado." -u low
fi
