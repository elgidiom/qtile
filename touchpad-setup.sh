#!/usr/bin/env sh

LAYOUT_RETRIES=10
SLEEP_SECS=1

apply_touchpad_settings() {
    xinput list --name-only 2>/dev/null | grep -i 'touchpad' || true
}

set_props() {
    DEVICE="$1"
    [ -z "$DEVICE" ] && return

    if xinput list-props "$DEVICE" 2>/dev/null | grep -q "libinput Tapping Enabled ("; then
        xinput set-prop "$DEVICE" "libinput Tapping Enabled" 1
    fi

    if xinput list-props "$DEVICE" 2>/dev/null | grep -q "libinput Natural Scrolling Enabled ("; then
        xinput set-prop "$DEVICE" "libinput Natural Scrolling Enabled" 1
    fi
}

i=0
while [ "$i" -lt "$LAYOUT_RETRIES" ]; do
    TOUCHPADS="$(apply_touchpad_settings)"
    if [ -n "$TOUCHPADS" ]; then
        echo "$TOUCHPADS" | while read -r DEVICE; do
            set_props "$DEVICE"
        done
        exit 0
    fi
    i=$((i + 1))
    sleep "$SLEEP_SECS"
done

exit 0
