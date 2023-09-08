from ...serializer import MenuButtonSerializer
from .obj import MenuButtonWebApp


class MenuButtonWebAppSerializer(MenuButtonSerializer):
    class Meta:
        model = MenuButtonWebApp
