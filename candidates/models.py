from django.db import models


class Candidate(models.Model):
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Other'),
    )

    STATUS_CHOICES = (
        (0, 'Applied'),
        (1, 'Shortlisted'),
        (2, 'Rejected'),
    )

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)
    years_of_exp = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    current_salary = models.DecimalField(max_digits=10, decimal_places=2)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name