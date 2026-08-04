from django.db import models


class Service(models.Model):
    """A service offering, managed in the admin and rendered dynamically."""

    title = models.CharField(max_length=80)
    tag = models.CharField(
        max_length=40,
        help_text='Short eyebrow label shown above the title, e.g. "Done for you".',
    )
    summary = models.TextField(
        help_text="One-paragraph pitch shown on the Services page and home teaser."
    )
    details = models.TextField(
        blank=True,
        help_text="Optional bullet points, one per line, shown on the Services page.",
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower shows first.")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    @property
    def detail_lines(self):
        return [line.strip() for line in self.details.splitlines() if line.strip()]


class Lead(models.Model):
    class Source(models.TextChoices):
        CONTACT = "contact", "Contact form"
        MEMBERS = "members", "Members waitlist"
        NEWSLETTER = "newsletter", "Newsletter"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        CLIENT = "client", "Client"
        CLOSED = "closed", "Closed / not a fit"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(
        max_length=20, choices=Source.choices, default=Source.CONTACT
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
    notes = models.TextField(
        blank=True, help_text="Internal notes — follow-ups, context, next steps."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        label = f"{self.name} <{self.email}>"
        if self.company:
            label += f" ({self.company})"
        return label

    @property
    def is_client(self):
        return self.status == self.Status.CLIENT


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
