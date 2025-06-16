# Home Automation

Scripts that I use for home stuff.

## Dependencies

- Python (tested on 3.13)
- [AutoHotKey](https://www.autohotkey.com/)
- [Display Changer II](https://display-changer-ii.en.lo4d.com/windows)

## TV Switcher

Helpful command: `dc2.exe -create=dc2_upper_only_config.xml`

To set up LGTV:

- Set up your Python environment, that should install the LGTV Python package + binary
- Run `lgtv scan` to find your TV
- Run `lgtv --ssl auth <tv_ip> <tv_name>` to authenticate, and accept the pairing request on the LG TV

Make sure you run AutoHotKey in administrator mode, otherwise it won't be able to start/stop some services to work around some dc2 issues.