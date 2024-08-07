from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import User, Object
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from extensions.utils import convert_size


# Create your views here.

@login_required
def home(request):
    context = {
        
    }
    response = render(request, 'account/home.html', context)
    refresh = RefreshToken.for_user(request.user)
    response.set_cookie("pwd" , '/root')
    response.set_cookie("jr" , str(refresh))
    response.set_cookie("ja" , str(refresh.access_token))
    return response


@login_required
def profile(request):
    context = {
        'state' : 'profile'
    }
    return render(request, 'account/profile.html', context)


class UploadFile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        userFile = request.FILES.get('user-file')
        userFilePath = request.POST.get('user-file-path')
        userFilePath = userFilePath.replace('"','')
        userFileType = request.POST.get('user-file-type')
        
        owner = request.user
        userFileName = userFile.name
        userFileSize = convert_size(userFile.size)

        newFile = Object()
        newFile.owner = owner
        newFile.name = userFileName
        newFile.iFile = True
        newFile.iFolder = False
        newFile.uploadFile = userFile
        newFile.iformat = userFileType
        newFile.size = userFileSize
        newFile.path = userFilePath
        newFile.save()
        
        content = {
            'msg' : "Your file successfully uploaded",
            'data' : None
        }
        
        return Response(content, status=status.HTTP_201_CREATED)



class CreateFolder(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pwd = request.POST.get('pwd')
        pwd = pwd.replace('"','')
        userFolderName = request.POST.get('folder-name')
        
        owner = request.user

        newFile = Object()
        newFile.owner = owner
        newFile.name = userFolderName
        newFile.iFile = False
        newFile.iFolder = True
        newFile.iformat = 'folder'
        newFile.path = pwd
        newFile.save()
        
        content = {
            'msg' : "Your folder created successfully",
            'data' : None
        }
        
        return Response(content, status=status.HTTP_201_CREATED)



class OurObjects(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pwd = request.POST.get('pwd')
        pwd = pwd.replace('"','')
        owner = request.user

        objects = Object.objects.filter(owner=owner, path=pwd).exclude(trash=True)
        
        alldata=[]
        
        for data in objects:
            if data.iFile:
                dataurl = data.uploadFile.url
            else:
                dataurl = None
            alldata.append({
                'id': data.id,
                'owner': data.owner.username,
                'name': data.name,
                'ifile': data.iFile,
                'ifolder': data.iFolder,
                'uploadfile': dataurl,
                'iformat': data.iformat,
                'size': data.size,
                'pwd': data.path,
                'stared': data.stared,
                'created': data.created.strftime('%Y-%m-%d %H:%M'),
                'updated': data.updated.strftime('%Y-%m-%d %H:%M')
            })
        
        content = {
            'msg' : "Your objects",
            'data' : alldata
        }
        
        return Response(content, status=status.HTTP_200_OK)