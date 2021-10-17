Hotkey, ^!m, SwitchToMonitor
Hotkey, ^!g, SwitchToGamingTv

SwitchToMonitor() {
    Run, node %A_WorkingDir%\lgtv.js switch_to_monitors
}

SwitchToGamingTv() {
    Run, node %A_WorkingDir%\lgtv.js switch_to_tv
}