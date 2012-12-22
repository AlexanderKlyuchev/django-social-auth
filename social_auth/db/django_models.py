"""Django ORM models for Social Auth"""
from django.db import models
from django.db.utils import IntegrityError

from social_auth.db.base import UserSocialAuthMixin, AssociationMixin, \
                                NonceMixin
from social_auth.fields import JSONField
from social_auth.utils import setting


# If User class is overridden, it *must* provide the following fields
# and methods work with django-social-auth:
#
#   username   = CharField()
#   last_login = DateTimeField()
#   is_active  = BooleanField()
#   def is_authenticated():
#       ...
USER_MODEL = setting('SOCIAL_AUTH_USER_MODEL') or \
             setting('AUTH_USER_MODEL') or \
             'auth.User'
UID_LENGTH = setting('SOCIAL_AUTH_UID_LENGTH', 255)


class UserSocialAuth(models.Model, UserSocialAuthMixin):
    """Social Auth association model"""
    user = models.ForeignKey(USER_MODEL, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    extra_data = JSONField(default='{}')
    default_foto=models.CharField(max_length=100)
    i_style=models.ManyToManyField("self",blank=True,symmetrical=False,related_name='my_stilist')
    i_pending_style=models.ManyToManyField("self",blank=True,symmetrical=False,related_name='my_pending_stilist')
    model=models.BooleanField(default=False)
    star=models.BooleanField(default=False)
    shop=models.BooleanField(default=False)
    fashionist=models.BooleanField(default=False)
    banned=models.BooleanField(default=False)
    aboutme=models.CharField(max_length=1000,blank=True)
    num_of_looks=models.IntegerField(default=0)
    received_votes=models.IntegerField(default=0)
    num_advices=JSONField(default='{"num_advices_datting":0,"num_advices_work":0,"num_advices_interview":0,"num_advices_learning":0,"num_advices_night":0,"num_advices_wedding":0,"num_advices_corporate":0,"num_advices_walking":0,"num_advices_thing":0,"num_advices_other":0}')
    count_advices=models.IntegerField(default=0)
    num_stilists=models.IntegerField(default=0)
    num_i_style=models.IntegerField(default=0)
    civility=models.IntegerField(default=0)
    num_agreed_advices=models.IntegerField(default=0)
    num_disagreed_advices=models.IntegerField(default=0)
    notifications=JSONField(default='{"my_looks_update":1,"style_req":1,"advice":1,"news":1,"push_notify":1}')
    latest_visit=models.DateTimeField(auto_now_add = True)
    num_positive_votes=models.IntegerField(default=0)
    city=models.CharField(null=True,blank=True,max_length=1000)
    country=models.CharField(null=True,blank=True,max_length=1000)
    bdate=models.IntegerField(null=True,blank=True)
    gender=models.IntegerField(null=True,blank=True)

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        app_label = 'social_auth'

    @classmethod
    def get_social_auth(cls, provider, uid):
        try:
            return cls.objects.select_related('user').get(provider=provider,
                                                          uid=uid)
        except UserSocialAuth.DoesNotExist:
            return None

    @classmethod
    def username_max_length(cls):
        field = UserSocialAuth.user_model()._meta.get_field('username')
        return field.max_length

    @classmethod
    def user_model(cls):
        return UserSocialAuth._meta.get_field('user').rel.to


class Nonce(models.Model, NonceMixin):
    """One use numbers"""
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        app_label = 'social_auth'


class Association(models.Model, AssociationMixin):
    """OpenId account association"""
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        app_label = 'social_auth'


def is_integrity_error(exc):
    return exc.__class__ is IntegrityError
