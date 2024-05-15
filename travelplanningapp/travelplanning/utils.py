from rest_framework.response import Response
from rest_framework import status


def ResponseBadRequest():
    return Response({
        'message': 'You dont have permission to do this!'
    }, status=status.HTTP_400_BAD_REQUEST)

def UniqueTogetherExcept(name):
    return Response({
        'message': f'{name} đã có trong danh sách điểm đến!'
    }, status=status.HTTP_400_BAD_REQUEST)