from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from instagram.users.models import User
from instagram.users.serializers import ListUserSerializer
from instagram.notifications.views import create_notification

class Images(APIView):

    def get(self, request, format=None):
        
        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            
            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:
            
            image_list.append(image)

        #sorted_list = sorted(image_list, key=get_key, reverse=True)
        sorted_list = sorted(image_list,key=lambda x: x.created_at,reverse=True)
        
        serializer = serializers.ImageSerializer(
            sorted_list, many=True, context={'request': request})

        return Response(status=200, data=serializer.data)

    def post(self, request, format=None):

        user =request.user

        serializer = serializers.InputImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(creator = user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#def get_key(image):
#    return image.created_at

class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image

        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)
    


    def delete(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeImage(APIView):

    def get(self, request, image_id, format=None):

        try:

            likes = models.Like.objects.filter(image__id=image_id)

            like_creator_ids = likes.values('creator_id')

            users = User.objects.filter(id__in=like_creator_ids)

            serializer = ListUserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            existing_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            existing_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:

            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            new_like.save()

            create_notification(user, found_image.creator,
                                'like', found_image)

            return Response(status=status.HTTP_201_CREATED)

class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        user=request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)

            #create_notification(user, found_image.creator, 'comment', found_image, request.data['message'])
            create_notification(user, found_image.creator,
                                'comment', found_image, serializer.data['message'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user=request.user

        try:
            comment = models.Comment.objects.get(id=comment_id,creator=user)
            comment.delete()

            return Response(status=status.HTTP_201_CREATED)

        except models.Comment.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):
        
        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(
                id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class Search(APIView):

    def get(self, request, format=None):
        hashtags = request.query_params.get('hashtags', None)
        
        if hashtags is not None:

            hashtags = hashtags.split(",")
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
