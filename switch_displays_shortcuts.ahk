Hotkey, ^!m, SwitchToMonitor
Hotkey, ^!g, SwitchToGamingTv
Hotkey, ^!u, SwitchToUpperOnly

SwitchToMonitor() {
    Run, node %A_WorkingDir%\lgtv.js switch_to_monitors
}

SwitchToGamingTv() {
    Run, node %A_WorkingDir%\lgtv.js switch_to_tv
}

SwitchToUpperOnly() {
    Run, node %A_WorkingDir%\lgtv.js switch_to_upper
}