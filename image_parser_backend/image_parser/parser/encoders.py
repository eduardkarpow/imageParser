from django.core.serializers.json import DjangoJSONEncoder
from parser.models import Image


class ImageEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Image):
            return {"id": o.pk, "name": o.name, "url": o.url}
        return super().default(o)
