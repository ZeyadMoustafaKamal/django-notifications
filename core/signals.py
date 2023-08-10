from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification

@receiver(post_save, sender=Notification)
def post_save_notification(sender, instance:Notification, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user_id = instance.user.id
        async_to_sync(channel_layer.group_send)(
            'notifications_{}'.format(user_id),
            {
                'type': 'notify',
                'title': instance.title,
                'content': instance.content,
                'created_at':str(instance.created_at.strftime('%b. %d, %Y, %I:%M %p'))
            }
        )


