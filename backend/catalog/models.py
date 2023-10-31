from django.db import models
from django.db.models import F

from .utils import slugify, code_validator


class HTMLCodeType(models.TextChoices):
    HEAD = "head"
    BODY = "body"
    FOOTER = "footer"


# Auto part size enum description
class AutoPartSizeType(models.TextChoices):
    INTEGER = "integer"
    RANGE = "range"
    CHOICE = "choice"


# Parse status enum description
class ParseStatus(models.TextChoices):
    DONE = "done"
    NEW = "new"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "brands"
        ordering = [F("name").asc()]

    def __str__(self):
        return self.name


class CategoryGroup(models.Model):
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    weight = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "category_groups"
        ordering = [F("weight").asc(nulls_last=True)]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CategoryGroup, self).save(*args, **kwargs)

    @property
    def enabled_categories(self):
        return Category.objects.filter(category_group=self, enabled=True).all()

    @classmethod
    def get_default_pk(cls):
        return cls.objects.get_or_create(name="Другое")[0].pk


class Size(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=AutoPartSizeType.choices, default=AutoPartSizeType.INTEGER)
    data = models.JSONField(blank=True, null=True)  # For choices, min, max, etc.
    detailed_description = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sizes"
        ordering = [F("name").asc()]

    def __str__(self):
        if self.description:
            return f"{self.name} ({self.description})"
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    category_group = models.ForeignKey(CategoryGroup, models.DO_NOTHING, default=CategoryGroup.get_default_pk, null=True)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    description_image = models.ImageField(blank=True, null=True)
    sizes = models.ManyToManyField(Size, blank=True)
    weight = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        ordering = [F("weight").asc(nulls_last=True)]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Image(models.Model):
    parsed_status = models.CharField(max_length=20, choices=ParseStatus.choices, default=ParseStatus.NEW)
    link = models.URLField(unique=True, max_length=255)
    image = models.ImageField(upload_to="images/%Y/%m/%d", unique=True, blank=True, null=True)
    sha256 = models.CharField(unique=True, max_length=64, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "images"


class AutoPart(models.Model):
    parsed_status = models.CharField(max_length=20, choices=ParseStatus.choices, default=ParseStatus.NEW)
    brand = models.ForeignKey(Brand, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    number = models.CharField(unique=True, max_length=50)
    sizes_values = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auto_parts"
        ordering = [F("number").asc()]

    def __str__(self):
        return self.number

    def get_image_url(self):
        if self.image:
            try:
                return self.image.image.url
            except ValueError:
                return None
        return None


class ExtraHTMLCode(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=HTMLCodeType.choices, default=HTMLCodeType.HEAD)
    code = models.TextField(validators=[code_validator])
    enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "head_or_body_html_codes"
        ordering = [F("created_at").asc()]

    def __str__(self):
        return f"{self.code[:50]}..."
