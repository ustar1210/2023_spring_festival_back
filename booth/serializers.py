from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = LogoImage
        fields = [
            "image",
        ]

class BoothListSerializer(serializers.ModelSerializer):

    like_cnt=serializers.IntegerField()
    logo_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_logo_image(self, instance):
        logoimage = instance.logoimages.first()
        try :
            logoimage_serializer = ImageSerializer(logoimage)
            return logoimage_serializer.data["image"]
        except:
            return None
    
    def get_is_liked(self, instance):
        #아직 구현 안함
        return None

    class Meta:
        model = Booth
        fields = [
            "id",
            "name",
            "type",
            "operator",
            "logo_image",
            "like_cnt",
            "start_at",
            "end_at",
            "location",
            "is_liked",
        ]

class BoothDetailSerializer(serializers.ModelSerializer):
    
    like_cnt=serializers.IntegerField()
    logo_image = serializers.SerializerMethodField()
    menu_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_logo_image(self, instance):
        logoimage = instance.logoimages
        try :
            logoimage_serializer = ImageSerializer(logoimage, many=True)
            outcome = []
            for data in logoimage_serializer.data:
                outcome.append(data["image"])
            return outcome
        except:
            return None
    
    def get_menu_image(self, instance):
        menuimage = instance.menuimages
        try :
            menuimage_serializer = ImageSerializer(menuimage, many=True)
            outcome = []
            for data in menuimage_serializer.data:
                outcome.append(data["image"])
            return outcome
        except:
            return None

    def get_is_liked(self, instance):
        #아직 구현 안함
        return None
    
    class Meta:
        model = Booth
        fields = [
            "id",
            "name",
            "type",
            "operator",
            "logo_image",
            "like_cnt",
            "start_at",
            "end_at",
            "location",
            "description",
            "menu",
            "menu_image",
            "concept",
            "is_liked",
            ]

class CommentReplySerializer(serializers.ModelSerializer):
    writer = serializers.CharField()
    password = serializers.CharField(write_only=True)
    content = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_deleted:
            representation['content'] = '삭제된 댓글입니다.'
        return representation
    
    def create(self, validated_data):
        comment = Comment.objects.get(id=self.context.get("view").kwargs.get("id"))
        validated_data["comment"] = comment
        return super().create(validated_data)
    
    class Meta:
        model = CommentReply
        fields = ['id', 'writer', 'password', 'content', 'created_at']
        
class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.CharField()
    password = serializers.CharField(write_only=True)
    content = serializers.CharField()
    replies = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_deleted:
            representation['content'] = '삭제된 댓글입니다.'
        return representation
    
    def get_replies(self, instance):
        replies = instance.commentreply_set.all()
        return CommentReplySerializer(replies, many=True).data
    
    def create(self, validated_data):
        booth = Booth.objects.get(id=self.context.get("view").kwargs.get("id"))
        validated_data["booth"] = booth
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = ['id', 'writer', 'password', 'content', 'created_at', 'replies']
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["booth", "key"]
