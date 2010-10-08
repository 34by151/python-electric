from django.db import models

class TED_history_second(models.Model):
    MTU = models.PositiveSmallIntegerField()
    DATE = models.DateTimeField() 
    POWER = models.DecimalField(max_digits=5, decimal_places=3)
    COST = models.DecimalField(max_digits=5, decimal_places=2)
    VOLTAGE = models.DecimalField(max_digits=5, decimal_places=1)
    FILTER = models.BooleanField()
#    def __unicode__(self):
#        return u'%s' % self.title

    class Meta:
        db_table = 'TED_history_second'


class TED_history_minute(models.Model):
    MTU = models.PositiveSmallIntegerField()
    DATE = models.DateTimeField() 
    POWER = models.DecimalField(max_digits=5, decimal_places=3)
    COST = models.DecimalField(max_digits=5, decimal_places=2)
    VOLTAGE = models.DecimalField(max_digits=5, decimal_places=1)

#    def __unicode__(self):
#        return u'%s' % self.title

    class Meta:
        db_table = 'TED_history_minute'

class TED_history_hour(models.Model):
    MTU = models.PositiveSmallIntegerField()
    DATE = models.DateTimeField() 
    POWER = models.DecimalField(max_digits=5, decimal_places=3)
    COST = models.DecimalField(max_digits=5, decimal_places=2)
    VMIN = models.DecimalField(max_digits=5, decimal_places=1)
    VMAX = models.DecimalField(max_digits=5, decimal_places=1)

#    def __unicode__(self):
#        return u'%s' % self.title

    class Meta:
        db_table = 'TED_history_hour'

class TED_history_day(models.Model):
    MTU = models.PositiveSmallIntegerField()
    DATE = models.DateTimeField() 
    POWER = models.DecimalField(max_digits=5, decimal_places=3)
    COST = models.DecimalField(max_digits=5, decimal_places=2)
    #PMIN = models.DecimalField(max_digits=5, decimal_places=3)
    #PMAX = models.DecimalField(max_digits=5, decimal_places=3)
    #CMIN = models.DecimalField(max_digits=5, decimal_places=2)
    #CMAX = models.DecimalField(max_digits=5, decimal_places=2)
    #VMIN = models.DecimalField(max_digits=5, decimal_places=1)
    #VMAX = models.DecimalField(max_digits=5, decimal_places=1)

#    def __unicode__(self):
#        return u'%s' % self.title

    class Meta:
        db_table = 'TED_history_day'

class TED_history_month(models.Model):
    MTU = models.PositiveSmallIntegerField()
    DATE = models.DateTimeField() 
    POWER = models.DecimalField(max_digits=8, decimal_places=3)
    COST = models.DecimalField(max_digits=5, decimal_places=2)
    #PMIN = models.DecimalField(max_digits=5, decimal_places=3)
    #PMAX = models.DecimalField(max_digits=5, decimal_places=3)
    #CMIN = models.DecimalField(max_digits=5, decimal_places=2)
    #CMAX = models.DecimalField(max_digits=5, decimal_places=2)
    #VMIN = models.DecimalField(max_digits=5, decimal_places=1)
    #VMAX = models.DecimalField(max_digits=5, decimal_places=1)

#    def __unicode__(self):
#        return u'%s' % self.title

    class Meta:
        db_table = 'TED_history_month'

class average_day(models.Model):
    MTU = models.PositiveSmallIntegerField()
    DATE = models.DateTimeField() 
    POWER7 = models.DecimalField(max_digits=5, decimal_places=3)
    POWER14 = models.DecimalField(max_digits=5, decimal_places=3)
    POWER21 = models.DecimalField(max_digits=5, decimal_places=3)
    POWER28 = models.DecimalField(max_digits=5, decimal_places=3)

class utility_bill(models.Model):
    DATE_START = models.DateField("Service From") 
    DATE_END = models.DateField("Service Through") 
    POWER_START = models.DecimalField("Previous Reading", max_digits=8, decimal_places=3)
    POWER_END = models.DecimalField("Current Reading", max_digits=8, decimal_places=3)
    COST = models.DecimalField("Electric Service Charge", max_digits=5, decimal_places=2)
