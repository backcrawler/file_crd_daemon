from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.renderers import JSONRenderer

import os

from .models import Pack
from .serializers import PackSerializer
from .renderers import PassthroughRenderer
from .utils import get_hash_name


class FileView(APIView):
    parser_classes = (FileUploadParser, JSONParser)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        try:
            file = Pack.objects.get(hash_name=kwargs['hash_name'])
        except Pack.DoesNotExist:
            return Response(status=404)
        response = FileResponse(open(file.f.path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename={}'.format(file.hash_name)
        return response

    def post(self, request):
        file_obj = request._request.FILES
        serializer = PackSerializer(data=file_obj)
        if serializer.is_valid():
            raw_data = serializer.validated_data['f'].file.read()
            serializer.validated_data['f'].file.seek(0)
            hash_name = get_hash_name(raw_data)
            serializer.validated_data['hash_name'] = hash_name
            f_obj = Pack.objects.filter(hash_name=hash_name).first()
            if f_obj:
                data = {'name': hash_name}
                return Response(data=data, status=201)  # user doesn't need to know whether it was the 1st time or not
            pack = serializer.save()                    # he only needs hash
            pack.hash_name = hash_name
            pack.save()
        else:
            return Response(status=400)
        data = {'name': hash_name}
        return Response(data=data, status=201)

    def delete(self, request, *args, **kwargs):
        try:
            file = Pack.objects.get(hash_name=kwargs['hash_name'])
        except Pack.DoesNotExist:
            return Response(status=404)
        file.f.delete()  # deleting file from drive
        file.delete()  # deleting DB object
        return Response(status=200)