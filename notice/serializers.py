from rest_framework import serializers

from .models import *

class NotificationImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = NotificationImage
        fields = ['image']
    

class NotificationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        # images = obj.notificationimage_set.all()
        # return NotificationImageSerializer(images, context=self.context, many=True).data
        image_urls = []
        images = obj.notificationimage_set.all().order_by('id')
        for image in images:
            url = image.image.url
            image_urls.append(url)
        return image_urls
    
    class Meta:
        model = Notification
        fields = ['id', 'title','type','content','created_at','images']