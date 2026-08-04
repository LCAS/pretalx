from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PluginApp(AppConfig):
    name = "pretalx_ref_wording"
    verbose_name = _("REF Wording Override")

    class PretalxPluginMeta:
        name = _("REF Wording Override")
        author = "LCAS"
        version = "0.1.0"
        visible = True
        description = _(
            "Provides an alternate English locale that renames terms like "
            "'Proposal' to 'Output' and 'Speaker' to 'Author', for use when "
            "running REF-style output review processes with pretalx. Does "
            "not change any workflow, permissions, or process logic."
        )
        category = "LANGUAGE"

    def ready(self):
        from . import signals  # noqa


PretalxPluginMeta = PluginApp.PretalxPluginMeta
