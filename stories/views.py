import django_rq

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Grapher, Story
from .serializers import AssetSerializer, GrapherSerializer
from .utils import asset_compress_worker

class UploadStoryView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        try:
            grapher = Grapher.objects.get(id=request.data['id'])
            grapher_id = grapher.id
        except Grapher.DoesNotExist:
            if 'grapher_first_name' in request.data.keys():
                grapher_first_name = request.data.get('grapher_first_name', '')
                grapher_last_name = request.data.get('grapher_last_name', '')
                if not grapher_first_name:
                    return Response({
                        'error': 'Grapher creation failed. No `first_name`'
                    }, status=status.HTTP_400_BAD_REQUEST)
                grapher = Grapher.objects.create(
                    first_name = grapher_first_name,
                    last_name = grapher_last_name
                )
                grapher_id = grapher.id
            else:
                return Response({
                    'error': 'Grapher id is not present'},
                    status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name', '')
        description = request.data.get('description', '')
        longitude = request.data.get('longitude', '')
        latitude = request.data.get('latitude', '')

        if not all([name, description, longitude, latitude]):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        asset_serializer = AssetSerializer(data=request.data)
        if asset_serializer.is_valid():
            asset_obj = asset_serializer.save()
            asset_obj.save()

            story_obj = Story.objects.create(
                grapher_id=grapher_id,
                asset_id=asset_obj.id,
                story_name=name,
                description=description,
                longitude=longitude,
                latitude=latitude,
            )

            payload = {
                'filename': asset_obj.asset_file.__str__(),
                'is_asset_image': asset_obj.is_asset_image,
                'grapher_id': grapher_id,
                'asset_id': asset_obj.id,
                'name': name,
                'description': description,
                'longitude': longitude,
                'latitude': latitude,

            }
            print(payload)
            queue = django_rq.get_queue()
            queue.enqueue(asset_compress_worker, **payload)

            return Response(data=payload, status=status.HTTP_201_CREATED)
