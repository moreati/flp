from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Blog(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    def __unicode__(self): return u'Blog (%s)' % self.name

class Post(models.Model):
    blog = models.ForeignKey(Blog)
    date = models.DateTimeField()
    length = models.IntegerField()
    post_id = models.CharField(max_length=1000)
    link = models.URLField(max_length=1000)
    author = models.CharField(max_length=255, null=True)
    def __unicode__(self): return u'Post %s' % (self.link,)

class Score(models.Model):
    post = models.ForeignKey(Post)
    value = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField() # stored so we can group on it because
    year = models.IntegerField()  # group by datepart() won't work across DBs
    attached_url = models.URLField(max_length=1000)
    def __unicode__(self): return u'Score %s ("%s") on %s' % (self.value, self.reason, self.post)

class User2Score(models.Model):
    user = models.ForeignKey(User)
    score = models.ForeignKey(Score)
    def __unicode__(self): return u'%s scored %s' % (self.user, self.score)

class User2Blog(models.Model):
    user = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    price = models.IntegerField()
    created_at = models.DateTimeField()
    def __unicode__(self): return u'User %s owning %s' % (self.user, self.blog)

class Log(models.Model):
    message = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self): return u'Log message "%s"' % (self.message)

class TwitterPostCount(models.Model):
    post = models.ForeignKey(Post)
    tweet_count_at_last_check = models.IntegerField(default=0)

@receiver(post_save, sender=User, dispatch_uid="log new user creation")
def user_saved(sender, **kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")
    if created and instance:
        from flp.common import publicLog
        publicLog("New shooter! New shooter @%s! Does our new shooter feel lucky?" % instance.username)
