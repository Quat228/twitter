from django.contrib import admin

from . import models


@admin.display(description='Short Text')
def get_short_text(obj):
    return f'{obj.text[:10]}...'


@admin.display(description='Short Text')
def get_short_text_20(obj):
    return f'{obj.text[:20]}...'


@admin.display(description='Fullname')
def get_profile_fullname(obj):
    fullname = obj.profile.user.get_full_name()
    return fullname if fullname else '-'


class TweetImagesInline(admin.TabularInline):
    model = models.TweetImages
    extra = 2


@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    # actions_on_bottom = True
    # actions_on_top = False
    empty_value_display = '--empty--'
    # exclude = ['profile', 'image']
    # fields = ['text', ]
    fields = (('text', 'profile'), 'image')
    list_display = ['id', get_profile_fullname, get_short_text, 'get_reactions_str', 'image', 'created_at']
    list_display_links = [get_short_text]  # указывается то, что есть только в list_display
    list_editable = ['image', ]
    list_filter = ['created_at', 'profile']
    list_per_page = 2
    save_as = True  # при обновлении поля, можно сохранить как новый объект
    save_on_top = False
    search_fields = ['text', 'profile__user__username__exact']
    sortable_by = ['created_at', 'id']
    inlines = [
        TweetImagesInline
    ]


@admin.register(models.Reaction)
class ReactionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReactionType)
class ReactionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    actions_on_top = False
    actions_on_bottom = True
    empty_value_display = '-'
    # emply_value_display не повлияет на поле get_profile_fullname потому что это вычисляемая функция,
    # и джанго не будет считать его даже если он вернет пустые значения
    fields = ('tweet', ('text', 'profile'))
    list_display = ['id', get_profile_fullname, get_short_text_20,
                    'created_at', 'get_reactions_str', 'tweet_id', 'profile']
    list_display_links = [get_short_text_20]
    list_editable = ['profile']
    list_filter = ['text', 'profile']
    sortable_by = ['id', 'created_at']

