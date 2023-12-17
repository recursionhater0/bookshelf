from typing import Any


class MethodMatchingViewSetMixin:
    action_serializers = None

    def get_serializer_class(self):
        base_serializer = super().get_serializer_class()
        return self.get_action_serializer_class().get(self.action, base_serializer)

    def get_action_serializer_class(self) -> dict[str, Any]:
        return self.action_serializers or {}
