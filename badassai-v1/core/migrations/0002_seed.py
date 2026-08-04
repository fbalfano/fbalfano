"""Seed the Site domain (per the django-standard SEO setup) and the three
launch services so the site renders complete on first deploy."""

from django.db import migrations

SERVICES = [
    {
        "title": "Agency",
        "tag": "Done for you",
        "summary": (
            "We design and build AI systems that actually ship — automations, "
            "agents, and workflows wired into the way your business already runs."
        ),
        "details": (
            "Workflow automation and AI agents\n"
            "Custom tools built around your operations\n"
            "Integration with the software you already use\n"
            "Handed over working, documented, and yours"
        ),
        "order": 1,
    },
    {
        "title": "Coaching",
        "tag": "Done with you",
        "summary": (
            "Hands-on training for you and your team, backed by a community of "
            "operators. Simple, practical AI skills you'll use on Monday morning."
        ),
        "details": (
            "Live workshops for teams and leaders\n"
            "One-on-one coaching for owners\n"
            "Community access between sessions\n"
            "Skills that stick — not tool-of-the-week tourism"
        ),
        "order": 2,
    },
    {
        "title": "Consulting",
        "tag": "Done right",
        "summary": (
            "Straight-talk strategy for leaders: where AI pays off in your "
            "business, where it doesn't, and a roadmap your team can actually execute."
        ),
        "details": (
            "AI opportunity assessment for your business\n"
            "Build-vs-buy guidance without vendor bias\n"
            "Rollout roadmaps your team can own\n"
            "Honest answers, even when the answer is 'don't'"
        ),
        "order": 3,
    },
]


def forwards(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=1, defaults={"domain": "badassai.ca", "name": "Bad Ass AI"}
    )
    Service = apps.get_model("core", "Service")
    for spec in SERVICES:
        Service.objects.update_or_create(title=spec["title"], defaults=spec)


def backwards(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Service.objects.filter(title__in=[s["title"] for s in SERVICES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [migrations.RunPython(forwards, backwards)]
