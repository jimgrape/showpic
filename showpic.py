# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 by ksy <910661511@qq.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# (this script requires WeeChat 0.3 or newer)
#
# History:
# 2018-11-19, ksy
#  version 0.6: add lastpic
# 2018-11-08, ksy <910661511@qq.com>
#  version 0.5: initial release

import weechat as w
import requests
import re
from PIL import Image
import json

SCRIPT_NAME    = "showpic"
SCRIPT_AUTHOR  = "ksy <910661511@qq.com>"
SCRIPT_VERSION = "0.6"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "show the pictures in buffer"
SCRIPT_COMMAND  = SCRIPT_NAME

settings = {
    'switch': 'on',  
    'exclude_list':'[]',
    'showall': 'on',
    'showtime': '3',
}

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,SCRIPT_DESC, "", ""):
    for option, default_value in settings.items():
        if not w.config_is_set_plugin(option):
            w.config_set_plugin(option, default_value)

    w.hook_command(SCRIPT_COMMAND,
        "show the pictures in buffer",
        "[on/off]",
        "switch the mode \n",
        " || on|off|exclude|include"
        " || showtime"
        " || showall on|off",
        "showpic_cb",
        '')

    showtime = int(w.config_get_plugin('showtime'))
    lastpic = {}
    exclude_list=json.loads(w.config_get_plugin('exclude_list'))

    w.hook_config("plugins.var.python." + SCRIPT_NAME + ".switch", "config_cb", "")
    hook = w.hook_print("", "", "", 1, "my_print_cb", "")

def show_pic(pic, size, x, y):
    global showtime
    im = Image.open(pic)
    ww = im.size[0]
    hh = im.size[1]
    if ww >= hh:
        hh = hh * size / ww
        ww = size
    else:
        ww = ww * size / hh
        hh = size
    cmd = "feh -g %sx%s+%s+%s --scale-down " % (ww, hh, str(x), str(y))
    w.hook_process(cmd + pic, showtime * 1000, "", "")

def my_print_cb(data, buffer, date, tags, displayed, highlight, prefix, message):
    showall = True if w.config_get_plugin('showall') == 'on' else False
    global lastpic, exclude_list
    if highlight or showall:
        msg = message
        if msg.startswith('[图片]('):
            pic = msg.lstrip('[图片](').rstrip(')')
            lastpic[buffer] = pic
            if buffer not in exclude_list:
                show_pic(pic, 500, 1300, 600)
        elif msg.startswith('[表情]('):
            pic = msg.lstrip('[表情](').rstrip(')')
            if buffer not in exclude_list:
                show_pic(pic, 200, 1000, 400)
        elif 'https://img.vim-cn.com/' in msg:
            msg = re.findall(r"(https:.*?(png|jpg|jpeg|gif))", msg)[0][0]
            r = requests.get(msg, stream=True)
            pic = '/tmp/picbed_tmp.png'
            with open(pic,'wb') as f:
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)
            lastpic[buffer] = pic
            if buffer not in exclude_list:
                show_pic(pic, 500, 1300, 600)
    return w.WEECHAT_RC_OK

def config_cb(data, option, value):
    global hook
    if value == 'on':
        hook = w.hook_print("", "", "", 1, "my_print_cb", "")
    else:
        w.unhook(hook)

    return w.WEECHAT_RC_OK

def showpic_cb(data, buffer, args):
    global showtime, exclude_list
    if args == '':
        show_pic(lastpic[buffer],500, 1300, 600)
    else:
        args = args.split()
        if args[0] == 'on':
            w.config_set_plugin('switch', 'on')
        elif args[0] == 'off':
            w.config_set_plugin('switch', 'off')
        elif args[0] == 'exclude':
            if buffer not in exclude_list:
                exclude_list.append(buffer)
                w.config_set_plugin('exclude_list', json.dumps(exclude_list))
            w.prnt(buffer, "pic won't show on this buffer")
        elif args[0] == 'include':
            if buffer in exclude_list:
                exclude_list.remove(buffer)
                w.config_set_plugin('exclude_list', json.dumps(exclude_list))
            w.prnt(buffer, "pic will show on this buffer again")
        elif args[0] == 'showall':
            if args[1] == 'on':
                w.config_set_plugin('showall', 'on')
            else:
                w.config_set_plugin('showall', 'off')
        elif args[0] == 'showtime':
            if args[1].isdigit():
                showtime = args[1]
                w.config_set_plugin('showtime', args[1])
    return w.WEECHAT_RC_OK

