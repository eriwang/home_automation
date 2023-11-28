Hotkey, ^!m, SwitchToMonitor
Hotkey, ^!g, SwitchToGamingTv
Hotkey, ^!u, SwitchToUpperOnly

SwitchToMonitor() {
    RunWait, %A_WorkingDir%\venv\Scripts\python.exe %A_WorkingDir%\main.py switch_to_monitors
}

SwitchToGamingTv() {
    RunWait, %A_WorkingDir%\venv\Scripts\python.exe %A_WorkingDir%\main.py switch_to_tv
}

SwitchToUpperOnly() {
    RunWait, %A_WorkingDir%\venv\Scripts\python.exe %A_WorkingDir%\main.py switch_to_upper
}