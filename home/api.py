import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import ApiSerializer
from .models import Api_Images
from .models import Image
from .count_wflys import *
import os


@csrf_exempt
@api_view(['POST', 'GET'])
def upload_image(request):
    if request.method == 'POST':
        serializer = ApiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        querryset = Api_Images.objects.all()
        serializer = ApiSerializer(querryset, many=True)
        return Response(serializer.data)


class ApiViewset(viewsets.ViewSet):
    """
    create:
        Upload Image and get count of Whiteflies.
    """
    serializer_class = ApiSerializer

    # list function returns all Images in the Database
    '''def list(self, request):
        querryset = Api_Images.objects.all()
        serializer = ApiSerializer(querryset, many=True)
        # obj = serializer.data
        # for o in obj:
            # return Response(o['image'])
        return Response(serializer.data)'''

    # create function adds a new Image  to the database
    def create(self, request):
        serializer = ApiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = serializer.data
            key = obj['id']
            params = 7, True, False
            points,wfly_image, img_pth = detect_matches_api(obj['image'])
            final_img, final_img_path = redraw_annotations(points, wfly_image, img_pth)
            # print("##################", os.path.basename(img_pth))
            res = {"image_name": os.path.basename(final_img_path), "trait_name": "whitefly count", "trait_value": str(len(points)), "image_link": "http://18.216.149.204/static/results/"+os.path.basename(final_img_path)}
            # return Response(json.dumps({"Count":str(len(points)),"Detected_Boxes":points}), status=status.HTTP_201_CREATED)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
