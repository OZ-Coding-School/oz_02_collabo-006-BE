from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from .serializers import PostSearchSerializer
from django.db.models import Q # OR, AND, NOT 연산 (WHERE 절)
from django.core.paginator import Paginator

class Search(APIView):
    def get(self, request):
        try:
            sort = request.GET.get('sort','new')
            page = int(request.GET.get('page', '1'))
            page_size = 12 

            keyword = request.GET.get('keyword', '').strip()
            search_list = Post.objects.filter(visible=True)

            if keyword:
                if keyword == '':  # keyword가 공백만 있는 경우
                    search_list = search_list.order_by('-created_at')[:24]
                elif keyword.startswith('#'): # 검색어에서 # 제거
                    keyword = keyword[1:]

                search_list = search_list.filter(
                    Q(hashtag__content__icontains=keyword) |
                    Q(content__icontains=keyword) |
                    Q(user__username__icontains=keyword)
                ).distinct()

                if not search_list.exists():
                    return Response({
                        "message": "검색 결과가 없습니다.",
                        'keyword': keyword
                    }, status=status.HTTP_404_NOT_FOUND)
                    
                # 정렬 옵션에 따라 결과 정렬
                if sort == 'new':
                    search_list = search_list.order_by('-created_at')[:24]
                elif sort == 'trending':
                    search_list = search_list.order_by('-likes')[:24]
                else:
                    return Response({
                        "error": {
                            "code": 400,
                            "message": "유효하지 않은 정렬 매개변수"
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                search_list = search_list.order_by('-created_at')[:24]

            paginator = Paginator(search_list, page_size)
            page_obj = paginator.get_page(page)

            serializer = PostSearchSerializer(search_list, many=True)

            return Response({
                "success": True,
                "code": 200,
                "message": "검색 성공",
                'keyword': keyword,
                "data": serializer.data,
                "total_results": len(serializer.data),
                "current_page": page_obj.number, # 현재 페이지
                "total_pages": paginator.num_pages # 총 페이지
            }, status=status.HTTP_200_OK)

        
        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)