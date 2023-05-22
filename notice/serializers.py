from rest_framework import serializers

from .models import *

class NotificationImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = NotificationImage
        fields = ['image']
    

class NotificationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, instance):
        request=self.context.get('request')
        noticeimage=instance.notificationimage_set.all().order_by('id')
        try:
            noticeimage_serializer=NotificationImageSerializer(noticeimage, many=True)
            outcome = []
            for data in noticeimage_serializer.data:
                image_url = request.build_absolute_uri(data["image"])
                outcome.append(image_url)
            return outcome
        except:
            return None
    
    class Meta:
        model = Notification
        fields = ['id', 'title','type','content','created_at','images']