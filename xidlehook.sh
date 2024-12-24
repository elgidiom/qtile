#!/usr/bin/env sh
# Only exported variables can be used within the timer's command.
export PRIMARY_DISPLAY="$(xrandr | awk '/ primary/{print $1}')"

# Run xidlehook
xidlehook \
    `# Don't lock when there's a fullscreen application` \
    --not-when-fullscreen \
    `# Don't lock when there's audio playing` \
    --not-when-audio \
    `# Dim the screen after 5 mins, undim if user becomes active` \
    --timer 300 \
    'xrandr --output "$PRIMARY_DISPLAY" --brightness .1' \
    'xrandr --output "$PRIMARY_DISPLAY" --brightness 1' \
    `# Undim & lock after 60 more seconds` \
    --timer 60 \
    'xrandr --output "$PRIMARY_DISPLAY" --brightness 1; i3lock -i ~/.config/qtile/wallpapers/lockscreen.jpg -F' \
    '' \
    `# Finally, suspend an hour after it locks` \
    --timer 3600 \
    'systemctl suspend' \
    ''
