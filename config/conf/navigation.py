from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Главная страница"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Пользователи"),
        "separator": True,
        "items": [
            {
                "title": _("Пользователи"),
                "icon": "groups_2",
                "link": reverse_lazy("admin:accounts_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
        ],
    },
    {
        "title": _("Раздел Книг"),
        "separator": True,
        "items": [
            {
                "title": _("Баннеры"),
                "icon": "campaign",
                "link": reverse_lazy("admin:havasbook_bannermodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Продукты"),
                "icon": "book",
                "link": reverse_lazy("admin:havasbook_bookmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
        ]
    },
    {
        "title": _("Категории"),
        "separator": True,
        "items": [
            {
                "title": _("Категории"),
                "icon": "view_list",
                "link": reverse_lazy("admin:havasbook_categorymodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Подкатегории"),
                "icon": "subdirectory_arrow_right",
                "link": reverse_lazy("admin:havasbook_subcategorymodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Пол"),
                "icon": "wc",
                "link": reverse_lazy("admin:havasbook_gendermodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Бренд"),
                "icon": "storefront",
                "link": reverse_lazy("admin:havasbook_brandmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
        ]
    },
    {
        "title": _("Раздел Заказов"),
        "separator": True,
        "items": [
            {
                "title": _("Заказы"),
                "icon": "shopping_cart",
                "link": reverse_lazy("admin:havasbook_ordermodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Элементы заказа"),
                "icon": "list_alt",
                "link": reverse_lazy("admin:havasbook_orderitemmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
        ]
    },
    {
        "title": _("Доставка"),
        "separator": True,
        "items": [
            {
                "title": _("Тип доставки"),
                "icon": "list_alt",
                "link": reverse_lazy("admin:havasbook_deliverymodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
        ]
    },
]
