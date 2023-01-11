from rest_framework import serializers
from notifications.models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    # from_profile = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Notifications
        fields = '__all__'
        depth = 1

    # @staticmethod
    # def get_from_profile(obj):
    #     return CommentatorSerializer(obj.from_profile, many=False).data
