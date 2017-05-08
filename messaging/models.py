from __future__ import unicode_literals

from django.db import models

MESSAGING_STATUS_CHOICES = (
    (1, 'Draft'),
    (2, 'Sent'),
    (3, 'Canceled'),
)

MESSAGING_TYPE = (
    (1, 'SMS'),
    (2, 'Email'),
    (3, 'Push'),
)