from django.db import models
from django.forms.widgets import Textarea
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet

from content_manager.abstract import SitesFacilesBasePage
from content_manager.managers import TagManager


class ContentPage(SitesFacilesBasePage):
    tags = ClusterTaggableManager(through="TagContentPage", blank=True)

    class Meta:
        verbose_name = _("Content page")

    settings_panels = SitesFacilesBasePage.settings_panels + [
        FieldPanel("tags"),
    ]


class TagContentPage(TaggedItemBase):
    content_object = ParentalKey("ContentPage", related_name="contentpage_tags")


@register_snippet
class Tag(TaggitTag):
    objects = TagManager()

    class Meta:
        proxy = True


class MonospaceField(models.TextField):
    """
    A TextField which renders as a large HTML textarea with monospace font.
    """

    def formfield(self, **kwargs):
        kwargs["widget"] = Textarea(
            attrs={
                "rows": 12,
                "class": "monospace",
                "spellcheck": "false",
            }
        )
        return super().formfield(**kwargs)


@register_setting(icon="code")
class AnalyticsSettings(BaseSiteSetting):
    class Meta:
        verbose_name = "Scripts de suivi"

    head_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name="Scripts de suivi <head>",
        help_text="Ajoutez des scripts de suivi entre les balises <head>.",
    )

    body_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name="Scripts de suivi <body>",
        help_text="Ajoutez des scripts de suivi vers la fermeture de la balise <body>.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("head_scripts"),
                FieldPanel("body_scripts"),
            ],
            heading="Scripts de suivi",
        ),
    ]


@register_setting(icon="cog")
class CmsDsfrConfig(BaseSiteSetting):
    class Meta:
        verbose_name = "Configuration du site"

    header_brand = models.CharField(
        "Institution (en-tête)",
        max_length=200,
        default="Intitulé officiel",
        help_text="""Intitulé du bloc-marques tel que défini sur la page
        https://www.gouvernement.fr/charte/charte-graphique-les-fondamentaux/le-bloc-marque""",
        blank=True,
    )
    header_brand_html = models.CharField(
        "Institution avec césure (en-tête)",
        max_length=200,
        default="Intitulé<br />officiel",
        blank=True,
        help_text="""Intitulé du bloc-marques avec des balises <br />
        pour affichage sur plusieurs lignes""",
    )
    footer_brand = models.CharField(
        "Institution (pied)",
        max_length=200,
        default="Intitulé officiel",
        blank=True,
    )

    footer_brand_html = models.CharField(
        "Institution avec césure (pied)",
        max_length=200,
        default="Intitulé<br />officiel",
        blank=True,
    )

    site_title = models.CharField(
        "Titre du site",
        max_length=200,
        default="Titre du site",
        blank=True,
    )
    site_tagline = models.CharField(
        "Sous-titre du site",
        max_length=200,
        default="Sous-titre du site",
        blank=True,
    )
    footer_description = models.TextField(
        "Description",
        default="",
        blank=True,
        help_text="Balises HTML autorisés",
    )

    search_bar = models.BooleanField("Barre de recherche dans l’en-tête", default=False)
    theme_modale_button = models.BooleanField("Choix du thème clair/sombre", default=False)
    mourning = models.BooleanField("Mise en berne", default=False)

    panels = [
        FieldPanel("header_brand"),
        FieldPanel("header_brand_html"),
        FieldPanel("footer_brand"),
        FieldPanel("footer_brand_html"),
        FieldPanel("site_title"),
        FieldPanel("site_tagline"),
        FieldPanel("footer_description"),
        FieldPanel("search_bar"),
        FieldPanel("mourning"),
        FieldPanel("theme_modale_button"),
    ]
