import argparse
import json

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
        config = json.loads(f.read())

    parser = argparse.ArgumentParser(description='My personal shortcuts for home automation.')
    parser.add_argument('command')
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()

    # This is busted in the package, fortunately the implementation is basically a one-liner
    if args.command == 'on':
        wakeonlan.send_magic_packet(config[TV_NAME]["mac"])
    else:
        kwargs = LGTV.parseargs(args.command, args.args)
        _exec_tv_command(args.command, config[TV_NAME], kwargs)


def _exec_tv_command(command: str, tv_config: dict, args: dict = None):
    args = args if args else {}
    remote = LGTV.LGTVRemote(TV_NAME, **tv_config, ssl=True)
    remote.connect()
    remote.execute(command, args)
    remote.run_forever()


if __name__ == '__main__':
    main()