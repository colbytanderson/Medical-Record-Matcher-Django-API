from django.db import models
from django.contrib.auth import get_user_model as user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = user_model()

class Record(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_owner')
    title = models.CharField(max_length=200, primary_key=True)
    editors = models.ManyToManyField(User, related_name='record_editor')
    confidenceScore = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ]
    )
    fullNameConfidenceScore = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ]
    )

    def save(self, *args, **kwargs):
        if not self.editors.exists():
            self.editors = self.editors.add(self.owner)
        super(Record, self).save(*args, **kwargs)

DATA_TYPES = (
    ("firstname", "firstname"),
    ("middlename", "middlename"),
    ('accountnumber', 'accountnumber'),
    ('lastname', 'lastname'),
    ('dob', 'dob'), # date of birth
    ('sex', 'sex'),
    ('street', 'street'),
    ('city', 'city'),
    ('state', 'state'),
    ('zip', 'zip'),
)

SKIP = (
    ("no", "no"),
    ("yes", "yes"),
)

class Column(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    confidenceScore = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ]
    )
    skip = models.CharField(choices=SKIP, max_length=3, default='no')
    dataType = models.CharField(choices=DATA_TYPES, max_length=40)
    index = models.IntegerField()


