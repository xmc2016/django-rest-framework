from django.shortcuts import render
from django.http import  HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import  Response
from rest_framework.decorators import action
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer,UserSerializer
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework import  status
from rest_framework.views import  APIView
from rest_framework import mixins
from rest_framework import  generics
from rest_framework import permissions
from django.contrib.auth.models import  User
from rest_framework import  renderers
from snippets.permissions import  IsOwnerOrReadOnly

from rest_framework import viewsets
from rest_framework.reverse import reverse
@api_view(['GET'])


def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
  
#
# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#     def get(self,request,*args,**kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

# class UserList(generics.ListAPIView):
#     queryset =  User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset =User.objects.all()
#     serializer_class = UserSerializer
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class SnippetViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`,`retrieve`,
        `update` and `destory` actions.
        Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    @action(detail=True,renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self,request,*args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    

    
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         content = {'error_message': "用户必须登陆！！"}
#         if self.request.user.username == '':
#             return Response(content, status=status.HTTP_403_FORBIDDEN, )
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#     def perform_create(self, serializer):
#         # owner=self.request.user
#         # if owner.username == '':
#         #     print("匿名用户！！")
#         #
#         #     return "403"
#         serializer.save(owner=self.request.user)
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]













# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#     def delete(self,request,*args,**kwargs):
#        return self.destroy(request,*args,**kwargs)






# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet
#     """
#     def get(self,request,format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets,many=True)
#         return Response(serializer.data)
#
#     def post(self,request,format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
# class SnippetDetail(APIView):
#     """
#     Retrieve,update or delete a snippet instance
#     """
#     def get_object(self,pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self,request,pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return  Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#








# @api_view(['GET','POST'])
# def snippet_list(request):
#     """
#     List all code snippets,or create a new snippet
#     :param request:
#     :return:
#     """
#     if request.method == 'GET':
#         snippets =  Snippet.objects.all()
#         serializer = SnippetSerializer(snippets,many=True)
#         return  Response(serializer.data)
#     elif request.method == 'POST':
#         #print(request.data)
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET','PUT','DELETE'])
# def snippet_detail(request,pk):
#     """
#     Retrieve, update or delete a code snippet.
#     :param request:
#     :param pk:
#     :return:
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

#https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#pulling-it-all-together
# 注解来标识一个视图可以被跨域访问
# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets,or create a ner snippet
#     :param request:
#     :return:
#     """
#     if request.method == "GET":
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets,many=True)
#         return JsonResponse(serializer.data,safe=False)
#     elif request.method =="POST":
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(date=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.errors,status=400)
#
#
#
#
# def snippet_detail(request,pk):
#     """
#     Retrieve,update or deleta a code snippet
#     :param request:
#     :param pk:
#     :return:
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == "GET":
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors,status=404)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)























