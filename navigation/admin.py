from django.contrib import admin
from .models import Menu, MenuItem

# Register your models here.
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', )
    list_filter = ('menu', 'parent')
    search_fields = ('title',)
    sortable_by = ('parent',)

admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)