import argparse
import json
import os
import time

import wakeonlan

import LGTV

TV_NAME = 'myTv'

# My own personal HDMI mappings - would be nice to take labels instead:
# - HDMI_1: PS5
# - HDMI_2: PC
# - HDMI_3: Nintendo Switch
# - HDMI_4: Chromecast (not labeled on my TV)


def main():
    # The LGTV package has some nice stuff I can use, but it also has some bugs. Roll my own stuff that wraps the stuff
    # that works.
    with open(LGTV.find_config()) as f:
        config = json.loads(f.read())[TV_NAME]

    parser = argparse.ArgumentParser(description='My personal shortcuts for home automation.')
    parser.add_argument('command')
    args = parser.parse_args()

    # TODO: doesn't argparse handle this natively?
    if args.command == 'switch_to_tv':
        # Turn on the TV. This is busted in the package, fortunately the implementation is a one-liner
        wakeonlan.send_magic_packet(config['mac'], ip_address='192.168.0.255')  # broadcast address

        # Wait for TV to turn on with timeout
        start_time = time.time()
        while not _is_tv_on(config):
            if time.time() - start_time > 5:
                raise TimeoutError("TV did not turn on within 5 seconds")
            time.sleep(0.1)

        time.sleep(0.5)  # Sleep an extra half second to ensure the TV can get requests
        _exec_tv_command(config, 'setInput', 'HDMI_2')

        time.sleep(2)  # Give the computer time to actually detect the TV before switching displays
        _switch_displays('dc2_tv_config.xml')

    elif args.command == 'switch_to_monitors':
        if _is_tv_on(config):
            # reset to Chromecast so I can still cast media to the TV later from phone/ google home
            _exec_tv_command(config, 'setInput', 'HDMI_4')

            time.sleep(1)
            _exec_tv_command(config, 'off')

        _switch_displays('dc2_monitors_config.xml')

    elif args.command == 'switch_to_upper':
        _switch_displays('dc2_upper_only_config.xml')

    else:
        raise argparse.ArgumentError(f'No known command "{args.command}" found')


def _is_tv_on(tv_config: dict) -> bool:
    # Ping the TV once, with a timeout of 250ms. Only works on Windows, the Linux command is different
    result = os.system(f'ping {tv_config["ip"]} -n 1 -w 250')
    return result == 0


def _exec_tv_command(tv_config: dict, command: str, *args):
    # LGTV does some fancy stuff in this function to generate args. Don't touch it
    kwargs = LGTV.parseargs(command, args)
    remote = LGTV.LGTVRemote(TV_NAME, **tv_config, ssl=True)
    remote.connect()
    remote.execute(command, kwargs)
    remote.run_forever()


def _switch_displays(config: str):
    os.system(f'E:\\Programs\\dc2.exe -configure={config}')

    # Display Changer has some annoyances where the audio doesn't swap with the display, this works around that
    os.system('cmd.exe /c "net stop audiosrv"')
    os.system('cmd.exe /c "net start audiosrv"')


if __name__ == '__main__':
    main()
