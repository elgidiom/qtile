#!/usr/bin/env sh

KBD_NAME="MX Keys Mini Keyboard"
LAYOUT="latam"
OPTIONS="ctrl:swapcaps"
STATE=""

apply_to_matching_keyboards() {
    # Aplica el layout/opciones a todos los dispositivos que coincidan y sean teclado.
    xinput list 2>/dev/null | awk -v name="$KBD_NAME" '
        $0 ~ name && $0 ~ "slave  keyboard" {
            for (i = 1; i <= NF; i++) {
                if ($i ~ /^id=/) {
                    gsub("id=", "", $i);
                    print $i;
                }
            }
        }
    ' | while read -r id; do
        [ -n "$id" ] && setxkbmap -device "$id" -layout "$LAYOUT" -option "$OPTIONS"
    done
}

while true; do
    CURRENT="$(xinput list --name-only 2>/dev/null | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g')"
    if [ "$CURRENT" != "$STATE" ]; then
        # Aplica al core y a dispositivos específicos (BT reconectados).
        setxkbmap -layout "$LAYOUT" -option "$OPTIONS"
        apply_to_matching_keyboards
        STATE="$CURRENT"
    fi
    sleep 2
done
