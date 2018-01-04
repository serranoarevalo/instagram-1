from rest_framework import serializers
from . import models
from instagram.users.models import User
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)



class SmallImageSerializer(serializers.ModelSerializer):
    """ Used for notifications """
    class Meta:
        model = models.Image
        fields = (
            'file',
        )


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'like_count',
            'comment_count'
        )

class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'profile_image',
        )

class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator'
        )

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer, TaggitSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'creator',
            'location',
            'caption',
            'comments',
            'like_count',
            'tags',
            'created_at'
        )

class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',
        )
