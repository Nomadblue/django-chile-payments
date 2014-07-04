# coding: utf-8
import datetime
from functools import partial
from django.db import models


class LogEntry(models.Model):
    magic1 = models.CharField(max_length=10, blank=True, null=True)  # transaction_id
    pid = models.PositiveIntegerField(default=0)
    magic2 = models.CharField(max_length=3, blank=True, null=True)
    action = models.CharField(max_length=10)
    magic3 = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=3)
    magic4 = models.CharField(max_length=20)
    message = models.TextField()
    payment = models.ForeignKey('getpaid.Payment')

    PROPERTIES = ('magic1', 'pid', 'magic2', 'action', 'magic3', 'date_str',
                  'time_str', 'ip', 'status', 'magic4', 'message')

    @property
    def date_str(self):
        return self.date.strftime("%d%m%Y")

    @date_str.setter
    def date_str(self, value):
        self.date = datetime.date(*map(int, (value[4:], value[2:4], value[:2])))

    @property
    def time_str(self):
        return self.time.strftime("%H%M%S")

    @time_str.setter
    def time_str(self, value):
        self.time = datetime.time(*map(int, (value[:2], value[2:4], value[4:])))

    @property
    def ip(self):
        return self.ip_address or "EMPTY"

    @ip.setter
    def ip(self, value):
        self.ip_address = value

    def __unicode__(self):
        template = "{:<10};{:>12};{:<3};{:<10};{:<40};{:<14};{:<6};{:<15};{:<3};{:<20};{}"
        properties = self.PROPERTIES
        return template.format(*map(partial(getattr, self), properties))

    @classmethod
    def from_line(cls, *args, **kwargs):
        line = kwargs.pop('line')
        entry = cls(**kwargs)
        properties = cls.PROPERTIES
        for property, value in zip(properties, map(str.strip, line.split(';'))):
            setattr(entry, property, value)
        return entry


class JournalEntry(models.Model):
    date = models.DateField()
    body = models.TextField()
    payment = models.OneToOneField('getpaid.Payment')

    @property
    def params(self):
        raw_params = self.body.split('#')
        return dict(map(lambda s: s.split('='), raw_params))

    def __unicode__(self):
        return self.body


def build_models(payment_class):
    """
    Here you can dynamically build a Model class that needs to have
    ForeignKey to Payment model
    """
    return []
