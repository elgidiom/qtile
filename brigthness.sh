#!/usr/bin/env sh

flag=false

max=21333

delta=2133

min=250

actual=$(cat /sys/class/backlight/intel_backlight/brightness)

# Haciendo mas suave bajar el brillo, pero no subirlo
if [ $((actual - 1000)) -lt $delta ] && [ "$1" = "-d" ]; then
    delta=500
fi

# Revisión de la flag para definir si es aumento o disminución.
if [ "$1" = "-u" ]; then
    flag=true
elif [ "$1" = "-d" ]; then
    flag=false
else
    echo "¿Subir o bajar el brillo?. Explicate, no soy adivino."
    exit 1
fi

# Se define el nuevo valor del brillo.
if $flag; then
    new=$((actual + delta))
else
    new=$((actual - delta))

fi

# Asegurandonos de que el brillo no exceda o llegue a cero.
if [ $new -lt $min ];
then
    new=$min
elif [ $new -gt $max ]; then
    new=$max
fi

echo $new | sudo tee /sys/class/backlight/intel_backlight/brightness
