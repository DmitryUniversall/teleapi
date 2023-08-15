from typing import TYPE_CHECKING
from teleapi.core.http.request.api_request import method_request
from teleapi.core.http.request.api_method import APIMethod

if TYPE_CHECKING:
    from teleapi.types.user import User


async def get_me() -> 'User':
    from teleapi.types.user import UserSerializer

    response, data = await method_request("GET", APIMethod.GET_ME)
    return UserSerializer().serialize(data=data['result'])
