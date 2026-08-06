from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PluginApp(AppConfig):
    name = "pretalx_ref_extensions"
    verbose_name = _("REF Extensions")

    class PretalxPluginMeta:
        name = _("REF Extensions")
        author = "LCAS"
        version = "0.1.0"
        visible = True
        description = _(
            "Adds API endpoints for silent, SSO-friendly batch user "
            "provisioning and speaker/reviewer assignment. Does not send "
            "invitation emails or change any core pretalx behaviour."
        )
        category = "INTEGRATION"


PretalxPluginMeta = PluginApp.PretalxPluginMeta
