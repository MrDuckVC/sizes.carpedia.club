from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import SearchBySizesForm, SearchByNumberForm
from .models import Category, CategoryGroup, AutoPart, AutoPartSizeType, ParseStatus, ExtraHTMLCode, HTMLCodeType


class ExtraHTMLCodeMixin:
    """
    Mixin for adding HTML code in body or head of every public page.
    """

    @staticmethod
    def get_head_html_code():
        """
        Get head HTML code.
        :return: QuerySet
        """
        return ExtraHTMLCode.objects.filter(type=HTMLCodeType.HEAD, enabled=True).all()

    @staticmethod
    def get_body_html_code():
        """
        Get body HTML code.
        :return: QuerySet
        """
        return ExtraHTMLCode.objects.filter(type=HTMLCodeType.BODY, enabled=True).all()

    @staticmethod
    def get_footer_html_code():
        """
        Get footer HTML code.
        :return: QuerySet
        """
        return ExtraHTMLCode.objects.filter(type=HTMLCodeType.FOOTER, enabled=True).all()

    def get_context_data(self, **kwargs):
        """
        Add head and body HTML code to context.
        :param kwargs: context
        :return: updated context
        """
        context = kwargs
        context["head_html_code"] = self.get_head_html_code()
        context["body_html_code"] = self.get_body_html_code()
        context["footer_html_code"] = self.get_footer_html_code()
        return context


def handler404(request, exception):
    return render(
        request,
        "catalog/404.html",
        status=404,
        context=ExtraHTMLCodeMixin.get_head_html_code(),
    )


class HomeView(ExtraHTMLCodeMixin, View):
    def get(self, request):
        return render(
            request,
            "catalog/home.html",
            context=self.get_context_data(),
        )


class CategoryGroupView(ExtraHTMLCodeMixin, View):
    def get(self, request, slug):
        category_group = get_object_or_404(CategoryGroup, slug=slug)
        if category_group.enabled_categories.count() >= 1:
            return render(
                request,
                "catalog/category_group.html",
                context=self.get_context_data(
                    category_group=category_group,
                ),
            )
        else:
            raise Http404()


class CategoryView(ExtraHTMLCodeMixin, View):
    def get(self, request, slug: str):
        category = get_object_or_404(Category, slug=slug, enabled=True)

        # Search by sizes form.
        search_by_sizes_form = SearchBySizesForm(category=category, data=request.GET)

        # Filter auto parts by sizes.
        auto_parts = AutoPart.objects.filter(category=category, parsed_status=ParseStatus.NEW)
        if search_by_sizes_form.is_valid():
            for field_name, value in search_by_sizes_form.cleaned_data.items():
                if value is not None and value != "":
                    # Filter by choice or integer parameter.
                    if category.sizes.get(name=field_name).type == AutoPartSizeType.INTEGER or category.sizes.get(name=field_name).type == AutoPartSizeType.CHOICE:
                        auto_parts = auto_parts.filter(sizes_values__contains={field_name: value})
                    # Filter by range parameter.
                    elif category.sizes.get(name=field_name).type == AutoPartSizeType.RANGE:
                        min_value, max_value = value.split("-")
                        auto_parts = auto_parts.filter(**{f"sizes_values__{field_name}__gte": min_value, f"sizes_values__{field_name}__lte": max_value})

        search_by_number_form = SearchByNumberForm(data=request.GET)
        if search_by_number_form.is_valid():
            number = search_by_number_form.cleaned_data["number"]
            if number != "":
                auto_parts = auto_parts.filter(number=number)

        # Pagination.
        page = request.GET.get("page", 1)
        paginator = Paginator(auto_parts, 15)
        page_obj = paginator.get_page(page)

        return render(
            request,
            "catalog/category.html",
            context=self.get_context_data(
                category=category,
                search_by_sizes_form=search_by_sizes_form,
                search_by_number_form=search_by_number_form,
                page_obj=page_obj,
            ),
        )


class AutoPartView(ExtraHTMLCodeMixin, View):
    def get(self, request, auto_part_id: int):
        auto_part = get_object_or_404(AutoPart, pk=auto_part_id)
        return render(
            request,
            "catalog/auto_part.html",
            context=self.get_context_data(
                auto_part=auto_part,
            ),
        )
