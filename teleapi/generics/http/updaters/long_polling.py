from typing import List

from teleapi.core.http.request import method_request
from teleapi.core.http.updaters import BaseUpdater
from teleapi.types.update.obj import Update
from teleapi.types.update.serializer import UpdateSerializer
from teleapi.core.http.request import APIMethod
from teleapi.core.utils.collections import clear_none_values


class LongPollingUpdater(BaseUpdater):
    def __init__(self, *, timeout: int = 60, offset: int = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.timeout = timeout
        self.offset = offset

    async def get_updates(self) -> List[Update]:
        params = clear_none_values({
            "timeout": self.timeout,
            "offset": self.offset,
            "allowed_updates": [upd.value for upd in self.allowed_updates] if self.allowed_updates else None
        })

        response, data = await method_request('GET', APIMethod.GET_UPDATES, params=params)

        if len(data['result']) == 0:
            return []

        updates = UpdateSerializer().serialize(data=data['result'], many=True)

        self.offset = updates[-1].id + 1

        return updates
