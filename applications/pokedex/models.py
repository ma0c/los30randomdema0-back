from django.db import models

from los30randomdema0.base_model import BaseModel


# Create your models here.


class Badge(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='badges/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='unique_name_index')
        ]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name_constraint')
        ]


class Profile(BaseModel):
    attendee = models.OneToOneField('registration.PossibleAttendees', related_name="profile", on_delete=models.CASCADE)
    badges = models.ManyToManyField(Badge, related_name='profiles')
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.attendee.name

    class Meta:
        indexes = [
            models.Index(fields=['attendee'], name='unique_attendee_index')
        ]
        constraints = [
            models.UniqueConstraint(fields=['attendee'], name='unique_attendee_constraint')
        ]


class Connection(BaseModel):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.attendee.name} follows {self.followed.attendee.name}"

    class Meta:
        indexes = [
            models.Index(fields=['follower', 'followed'], name='unique_follower_followed_index')
        ]
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follower_followed_constraint')
        ]
