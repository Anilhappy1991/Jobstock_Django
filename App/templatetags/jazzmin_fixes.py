"""
Fixed Jazzmin template tags for Django 6.0 compatibility.
Overrides jazzmin_paginator_number to fix format_html() issue.
"""
from django import template
from django.contrib.admin.views.main import ChangeList, PAGE_VAR
from django.utils.safestring import SafeText, mark_safe

register = template.Library()


@register.simple_tag
def jazzmin_paginator_number(change_list: ChangeList, i: int) -> SafeText:
    """
    Generate an individual page index link in a paginated list.
    Fixed for Django 6.0 - uses mark_safe instead of format_html.
    """
    html_str = ""
    start = i == 1
    end = i == change_list.paginator.num_pages
    spacer = i in (".", "…")
    current_page = i == change_list.page_num

    if start:
        link = change_list.get_query_string({PAGE_VAR: change_list.page_num - 1}) if change_list.page_num > 1 else "#"
        html_str += """
        <li class="page-item previous {disabled}">
            <a class="page-link" href="{link}" data-dt-idx="0" tabindex="0">«</a>
        </li>
        """.format(link=link, disabled="disabled" if link == "#" else "")

    if current_page:
        html_str += """
        <li class="page-item active">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">{num}</a>
        </li>
        """.format(num=i)
    elif spacer:
        html_str += """
        <li class="page-item disabled">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="4" tabindex="0">…</a>
        </li>
        """
    else:
        link = change_list.get_query_string({PAGE_VAR: i})
        html_str += """
        <li class="page-item">
            <a class="page-link" href="{link}" data-dt-idx="5" tabindex="0">{num}</a>
        </li>
        """.format(link=link, num=i)

    if end:
        link = change_list.get_query_string({PAGE_VAR: change_list.page_num + 1}) if change_list.page_num < change_list.paginator.num_pages else "#"
        html_str += """
        <li class="page-item next {disabled}">
            <a class="page-link" href="{link}" data-dt-idx="6" tabindex="0">»</a>
        </li>
        """.format(link=link, disabled="disabled" if link == "#" else "")

    # Use mark_safe instead of format_html for Django 6.0 compatibility
    return mark_safe(html_str)
