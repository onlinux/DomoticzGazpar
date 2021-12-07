# -*- coding: utf-8 -*-
# (C) v1.0.0 2021-12-07 Onlinux
"""Create a special domoticz HTTPhandler to be used with logging module
All logging messages will be sent to domoticz log thru http call
"""

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging.handlers


class domoticzHandler(logging.handlers.HTTPHandler):
    def __init__(self, host, prefix):
        super().__init__(host='localhost:8080', url='/json.htm')
        self.host = host
        self.prefix = prefix

    def mapLogRecord(self, record):
        if self.formatter is None:
            text = record.msg % record.args
        else:
            text = self.formatter.format(record)

        level = (
            '2' if record.levelname == 'DEBUG' else
            '1' if record.levelname == 'INFO' else
            '4' if record.levelname == 'WARNING' else
            '4' if record.levelname == 'ERROR' else
            '4' if record.levelname == 'CRITICAL' else
            ''
        )

        return {
            'level': f'{level}',
            'type': 'command',
            'param': 'addlogmessage',
            'message': f'{self.prefix} ' f'{record.levelname} ' f'{text}'
        }
