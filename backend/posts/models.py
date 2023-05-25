import io

from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.core.files import File

from PIL import Image, ImageDraw, ImageFont

from accounts.models import Profile


def process_image(img, text=None, ext='png', font_type='arial.ttf',
                  font_size=32, x=0, y=0, new_height=None, new_width=None):
    image = Image.open(img)

    width, height = image.size
    if new_width:
        new_height = int(height * new_width / width)

    elif new_height:
        new_width = int(width * new_height / height)

    if new_width and new_height:
        image.resize(new_width, new_height)

    if text:
        img_draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_type, size=font_size)
        img_draw.text((x, y), text, font=font)

    image_io = io.BytesIO()
    image.save(image_io, ext)
    return File(image_io, f'image.{ext}')


def tweet_image_store(instance, filename):
    return f"profile/{instance.profile.user.username}/{timezone.now().strftime('%Y%m%d_%H%M')}/{filename}"


def reply_image_store(instance, filename):
    return f"profile/{instance.profile.user.username}/{instance.tweet.text[:15]}/{filename}"


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    image = models.ImageField(upload_to=tweet_image_store, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Твит'
        verbose_name_plural = 'Твиты'

    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image, text='Property of me', font_size=24, x=10, y=10)
        super().save(*args, **kwargs)

    def all_reactions(self):
        result = {}
        for r_type in ReactionType.objects.all():
            result[r_type.name] = 0
        del result['No reaction']
        for reaction in self.reactions.all():
            result[reaction.type.name] += 1
        return result

    def get_reactions(self):
        reactions = self.reactions.all()
        result = {}
        for reaction in reactions:
            if result.get(reaction.type.name):
                result[reaction.type.name] += 1
            else:
                result[reaction.type.name] = 1
        return result

    @admin.display(description='Reactions')
    def get_reactions_str(self):
        reactions = self.get_reactions()
        return str(reactions)

    def __str__(self):
        return self.text


class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='replies')
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    image = models.ImageField(upload_to=reply_image_store, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image, text='Reply', font_size=16, x=30, y=50)
        super().save(*args, **kwargs)

    def get_reactions(self):
        reactions = self.reply_reactions.all()
        result = {}
        for r_type in ReactionType.objects.all():
            result[r_type.name] = 0
        del result['No reaction']
        for reaction in reactions:
            result[reaction.type.name] += 1
        return result

    @admin.display(description='reactions')
    def get_reactions_str(self):
        return str(self.get_reactions())

    def __str__(self):
        return self.text


class ReactionType(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Reaction(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='reactions')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.ForeignKey(ReactionType, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return f'{self.tweet} - {self.profile} - {self.type}'

    class Meta:
        unique_together = ['tweet', 'profile']


class ReplyReaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.ForeignKey(ReactionType, on_delete=models.SET_DEFAULT, default=1)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='reply_reactions')

    def __str__(self):
        return f'{self.reply} - {self.profile} - {self.type}'

    class Meta:
        unique_together = ['reply', 'profile']


def tweet_multiple_image_store(instance, filename):
    return f"profile/{instance.tweet.profile.user.username}/{instance.tweet.id}/{filename}"


class TweetImages(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=tweet_multiple_image_store)
