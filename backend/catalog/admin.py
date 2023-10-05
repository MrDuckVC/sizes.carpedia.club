from django.contrib import admin

from .models import AutoPart, Brand, Category, Image, CategoryGroup, Size, ExtraHTMLCode


# Register your models here.


class AutoPartAdmin(admin.ModelAdmin):
    list_display = ("number", "brand", "category", "parsed_status", "created_at", "updated_at")
    list_filter = ("parsed_status", "brand", "category")
    search_fields = ("number", "brand__name", "category__name")

    def label_brand(self, obj):
        return obj.brand.name


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "weight", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_group", "slug", "weight", "created_at", "updated_at")
    search_fields = ("name", "category_group__name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ("link", "parsed_status", "created_at", "updated_at")
    list_filter = ("parsed_status",)
    search_fields = ("link",)


class SizesAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "type", "data", "created_at", "updated_at")
    list_filter = ("type",)
    search_fields = ("name", "description")


class ExtraHTMLCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "enabled", "created_at", "updated_at")
    search_fields = ("name", "code")


admin.site.register(AutoPart, AutoPartAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Size, SizesAdmin)
admin.site.register(ExtraHTMLCode, ExtraHTMLCodeAdmin)
