from django.contrib import admin
from models import utility_bill
##from django import forms

##admin.site.register(utility_bill)

class UtilityBillAdmin(admin.ModelAdmin):
##    fields = ('DATE_START', 'DATE_END', 'POWER_START', 'POWER_END', 'COST')
    fieldsets = [
        ('Service period', {'fields': ['DATE_START', 'DATE_END']}),
        ('Meter reading', {'fields': ['POWER_START', 'POWER_END']}),
        ('Service Cost', {'fields': ['COST']}),
        ]

    list_display = ('DATE_END', 'COST')
    date_hierarchy = 'DATE_END'


##    list_display = 
##    list_filter = 
##    form = 
##
admin.site.register(utility_bill, UtilityBillAdmin)

##class PortfolioImageForm(forms.ModelForm):
####    image = forms.ImageField(widget=AdminImageWidget())
####
####    class Meta:
####        model = PortfolioImage
####
##class PortfolioImageInline(admin.TabularInline):
##	model=PortfolioImage
##	Extra=5
##	form = PortfolioImageForm

##class PortfolioImageAdmin(admin.ModelAdmin):
##	fields = ('image', 'alt_attribute', 'title_attribute',)
##	list_display = ['image', 'alt_attribute', 'title_attribute',] 
##	list_filter = ['portfolioitem']
##	form = PortfolioImageForm

##class PortfolioHeaderForm(forms.ModelForm):
##	image_header = forms.ImageField(widget=AdminImageWidget())
##	
##	class Meta:
##		model = PortfolioItem  
##	
##class PortfolioItemAdmin(multilingual.ModelAdmin):
##    
##	fields = ('slug', 'image_header')
##	form = PortfolioHeaderForm
##	    	
##	#inline display...
##	model = PortfolioItem
##	inlines = [PortfolioImageInline]
       


