import sys

import wakeonlan

import LGTV

sys.argv = ['lgtv', '--ssl', '--name', 'myTv', 'on']

LGTV.main()
