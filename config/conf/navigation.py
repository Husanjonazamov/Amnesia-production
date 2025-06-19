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
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Foydalanuvchilar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Foydalanuvchilar"),
                "icon": "groups_2",
                "link": reverse_lazy("admin:accounts_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            # {
            #     "title": _("Foydalanuvchilar"),
            #     "icon": "person_add",
            #     "link": reverse_lazy("admin:auth_user_changelist"),
            #     "permission": lambda request: user_has_group_or_permission(
            #         request.user, "view_user"
            #     ),
            # },
        ],
    },
    {
        "title": _("Kitoblar bo'limi"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Bannerlar"),
                "icon": "campaign", 
                "link": reverse_lazy("admin:havasbook_bannermodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Kitoblar"),
                "icon": "book",  # Kitoblar uchun mos icon
                "link": reverse_lazy("admin:havasbook_bookmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
        ]

    },
    {
        "title": _("Kategorylar"),
        "separator": True,
        "items": [
            {
                "title": _("Kategoryalar"),
                "icon": "view_list",  # Asosiy kategoriya uchun
                "link": reverse_lazy("admin:havasbook_categorymodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("SubCateogry"),
                "icon": "subdirectory_arrow_right",  # Subkategoriya uchun
                "link": reverse_lazy("admin:havasbook_subcategorymodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Gender"),
                "icon": "wc",  # Gender uchun
                "link": reverse_lazy("admin:havasbook_gendermodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Brand"),
                "icon": "storefront",  # Brendlar uchun
                "link": reverse_lazy("admin:havasbook_brandmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
        ]
    },

    # {
    #     "title": _("Savatlar bo'limi"),
    #     "separator": True,  # Top border
    #     "items": [
    #         {
    #             "title": _("Foydalanuvchi Savati"),
    #             "icon": "shopping_cart",  # Mos icon (shopping cart)
    #             "link": reverse_lazy("admin:havasbook_cartmodel_changelist"),
    #             "permission": lambda request: user_has_group_or_permission(
    #                 request.user, "view_user"
    #             ),
    #         },
    #         {
    #             "title": _("Savatdagi elementlar"),
    #             "icon": "list_alt",  # Mos icon (list of items)
    #             "link": reverse_lazy("admin:havasbook_cartitemmodel_changelist"),
    #             "permission": lambda request: user_has_group_or_permission(
    #                 request.user, "view_group"
    #             ),
    #         },
    #     ]
    # },
    {
        "title": _("Buyurtmalar bo'limi"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Buyurtmalar"),
                "icon": "shopping_cart",  # Mos icon (shopping cart)
                "link": reverse_lazy("admin:havasbook_ordermodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("Buyurtma elementlar"),
                "icon": "list_alt",  # Mos icon (list of items)
                "link": reverse_lazy("admin:havasbook_orderitemmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            # {
            #     "title": _("Oldindan Buyurtmalar"),
            #     "icon": "list_alt",  # Mos icon (list of items)
            #     "link": reverse_lazy("admin:havasbook_preordermodel_changelist"),
            #     "permission": lambda request: user_has_group_or_permission(
            #         request.user, "view_group"
            #     ),
            # },
        ]
    },
    {
        "title": _("Yetkazib berish"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Yetkazib berish Turi"),
                "icon": "list_alt",  # Mos icon (list of items)
                "link": reverse_lazy("admin:havasbook_deliverymodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
        ]
    },
]
