import os
import cv2
import django_rq
import moviepy.editor as mp

from PIL import Image
from django.conf import settings

from stories.models import Story

def asset_compress_worker(*args, **kwargs):
    if kwargs.get('is_asset_image'):
        compress_image(**kwargs)
    else:
        compress_video(**kwargs)

def compress_image(**kwargs):
    image_name = kwargs.get('filename')
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)

    try:
        story_obj = Story.objects.get(
            asset_id=kwargs.get('asset_id'),
            grapher_id=kwargs.get('grapher_id')
        )
    except Story.DoesNotExist:
        return False

    local_image_obj = Image.open(image_path)
    image_size = local_image_obj.size
    width, height = image_size

    if width < 600 and height < 1200:
        return False

    local_image_obj = local_image_obj.resize((600, 1200), Image.ANTIALIAS)
    local_image_obj.save(image_path)

    story_obj.save()

    return True


def compress_video(**kwargs):
    video_name = kwargs.get('filename')
    video_path = os.path.join(settings.MEDIA_ROOT, video_name)
    cap = cv2.VideoCapture(video_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if height < 480:
        return None
    clip = mp.VideoFileClip(video_path)
    clip_resized = clip.resize(height=480)
    clip_resized.write_videofile(video_path)

