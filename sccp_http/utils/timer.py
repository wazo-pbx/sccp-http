# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio

class Timer:
    def __init__(self, timeout, callback, repeating=True):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())
        self._stop_flag = False
        self._repeating = repeating

    async def _job(self):
        while not self._stop_flag:
            await self._callback()

            if not self._repeating:
                self._stop_flag = True

            await asyncio.sleep(self._timeout)


    def cancel(self):
        self._stop_flag = True
        self._task.cancel()

    def reset(self):
        self._stop_flag = False
        self._task = asyncio.ensure_future(self._job())
