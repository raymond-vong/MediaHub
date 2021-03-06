from django.db import models
from django.db.models import fields
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import AutoField, BooleanField, CharField, PositiveSmallIntegerField, SmallAutoField, SmallIntegerField, TextField, URLField
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator

class CategoryGenre(models.Model):
    categoryGenreID = CharField(primary_key=True, max_length=20)
    categoryGenreDescription = TextField()

class Media (models.Model):
    mediaID = models.AutoField(primary_key=True)
    mediaTitle = models.CharField(max_length=50)
    mediaRelease = models.DateField()
    categories = models.ManyToManyField(CategoryGenre, blank=True)

    def __str__ (self):
        return self.mediaTitle

class Book (Media):
    author = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=13)

    def __str__(self):
        return self.author

class Movie (Media):
    medium = models.CharField(max_length=30)
    director = models.CharField(max_length=30)

    def __str__(self):
        return self.medium

class VideoGame(Media):
    pass

class Show(Media):
    pass

class VideoGameConsole (models.Model):
    videoGameConsoleMediaID = ForeignKey(VideoGame, on_delete=CASCADE)
    console = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.console

class ShowSeasons (models.Model):
    showSeasonMediaID = ForeignKey(Show, on_delete=CASCADE)
    showSeason = PositiveSmallIntegerField(unique=True)

class Platform (models.Model):
    platformID = AutoField(primary_key=True)
    platformName = models.CharField(max_length=20)
    platformHosts = models.ManyToManyField(Media, blank=True)

    def __str__(self) -> str:
        return self.platformName

class Physical (Platform):
    physicalDescription = TextField()

class Device (Platform):
    deviceDescription = TextField()

class Website (Platform):
    websiteDescription = URLField()

class Review (models.Model):
    reviewID = AutoField(primary_key=True)
    rating = SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MinValueValidator(100)
        ]
    )
    comment = TextField()

class User (models.Model):
    userID = CharField(max_length=50, primary_key=True)
    userName = CharField(max_length=50)
    userPassword = CharField(max_length=30)
    userUsesPlatform = models.ManyToManyField(Platform, blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.userID

class Admin (models.Model):
    adminID = models.CharField(max_length=50, primary_key=True)
    adminFirstName = models.CharField(max_length=30)
    adminLastName = models.CharField(max_length=30)
    adminPassword = models.CharField(max_length=30)
    adminManagesUsers = models.ManyToManyField(User, blank=True)
    adminManagesMedia = models.ManyToManyField(Media, blank=True)

class Playlist (models.Model):
    playListUser = ForeignKey(User, on_delete=CASCADE)
    playListName = CharField(max_length=30)
    playListContains = models.ManyToManyField(Media, blank=True)
    
    def __str__(self) -> str:
        return self.playListName
        
    class META:
        UniqueConstraint(fields=['playListUserID', 'playListName'],name='uniqueUserPlaylist')


class Permission (models.Model):
    userID = ForeignKey(User, on_delete=CASCADE)
    ratingPerm = BooleanField()
    commentsPerm = BooleanField()
    addMediaPerm = BooleanField()

class Suggestions (models.Model):
    suggestorsUserID = ForeignKey(User, related_name ='suggestor', on_delete=CASCADE)
    suggesteeUserID = ForeignKey(User, related_name ='suggestee',  on_delete=CASCADE)
    suggestedMediaID = ForeignKey(Media, on_delete=CASCADE)

class Shares (models.Model):
    creatorUserID = ForeignKey(User, related_name ='creator', on_delete=CASCADE)
    sharedUserID = ForeignKey(User, related_name ='shared',  on_delete=CASCADE)
    sharedPlaylistID = ForeignKey(Playlist, on_delete=CASCADE)

class Rates (models.Model):
    rateUserID = ForeignKey(User, on_delete=CASCADE)
    rateReviewID = ForeignKey(Review, on_delete=CASCADE)
    rateMediaID = ForeignKey(Media, on_delete=CASCADE)

class Owns (models.Model):
    ownsUserID = ForeignKey(User, on_delete=CASCADE)
    ownsPlatformID = ForeignKey(Platform, on_delete=CASCADE)
    ownsMediaID = ForeignKey(Media, on_delete=CASCADE)
