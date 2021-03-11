from django.contrib import admin
from .models import *
from csvexport.actions import csvexport
# Register your models here.
class item(admin.ModelAdmin):
    list_display = ('title','price','category','brand','status','label','image')
    search_fields = ['title','description']
    list_filter = ('status','label','category','brand')
    list_per_page = 10
    actions = [csvexport]
admin.site.register(Item,item)

class Categorys(admin.ModelAdmin):
    list_display = ('name','slug','image')
    search_fields = ['name']
    list_per_page = 10
admin.site.register(Category,Categorys)

admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)

admin.site.register(Cart)
admin.site.register(Contact)