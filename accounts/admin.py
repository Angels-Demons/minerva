from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from accounts import models
from accounts.models import Profile
from django.urls import reverse
from django.utils.html import format_html
User = get_user_model()


def is_owner(user):
    (owners_group, created) = Group.objects.get_or_create(name='owners')
    if user in owners_group.user_set.all():
        print("user is owner")
        return True
    print("user is not owner")
    return False


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'is_active', 'is_admin', 'is_staff', 'timestamp', 'get_credit')

    def get_credit(self, obj):
        return obj.profile.credit

    get_credit.short_description = 'Credit'
    get_credit.admin_order_field = 'profile__credit'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'credit', 'app_version', 'name', 'email', 'timestamp')
    search_fields = ('user__phone', 'app_version')
    # list_filter = ['site']

    # def top_up(self, obj):
    #     try:
    #         link = "/../../../zarinpal/top_up/" + str(obj.id) + "/" + str(obj.user.phone)
    #         # link = reverse("admin:scooter_ride_change", args=[obj.current_ride.id])  # model name has to be lowercase
    #         return format_html(
    #             """<input type="button" style="margin:2px;2px;2px;2px;" value="%s" onclick = "location.href=\'%s\'"/>"""
    #             % ("top up", link))
    #     except Exception as e:
    #         print(e)
    #         return None
    #
    # top_up.allow_tags = True
    # top_up.label = "top up"
    #
    # def _current_ride(self, obj):
    #     try:
    #         link = reverse("admin:scooter_ride_change", args=[obj.current_ride.id]) #model name has to be lowercase
    #         return format_html(u'<a href="%s">%s</a>' % (link, obj.current_ride))
    #     except:
    #         return None
    # _current_ride.allow_tags = True

    def get_queryset(self, request):
        # if is_owner(request.user):
        #     return super().get_queryset(request).filter(site=request.user.owner.site)
        return super().get_queryset(request)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
