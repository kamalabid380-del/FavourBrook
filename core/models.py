from django.db import models


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=120, default="Favourbrook")
    tagline = models.CharField(max_length=120, default="Piccadilly Arcade, London")
    logo = models.ImageField(upload_to="home/", blank=True, help_text="Dark logo for light backgrounds.")
    logo_white = models.ImageField(upload_to="home/", blank=True, help_text="White logo for the footer.")
    announcement = models.CharField(max_length=160, default="Free shipping over £300 · No unexpected international duties")
    currency_symbol = models.CharField(max_length=4, default="£")
    email = models.EmailField(default="customerservices@favourbrook.com")
    phone = models.CharField(max_length=40, default="+44 (0)20 7493 5464")
    address = models.CharField(max_length=200, default="18-19 Piccadilly Arcade, London SW1Y 6NH")
    instagram_url = models.URLField(blank=True, default="https://www.instagram.com/favourbrook")
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/favourbrook")
    pinterest_url = models.URLField(blank=True, default="https://www.pinterest.com/favourbrook")
    about_text = models.TextField(default="Favourbrook perfectly craft made-to-measure menswear and womenswear from our flagship store at 18-19 Piccadilly Arcade, London. Discover waistcoats, eveningwear and occasionwear, handmade in the UK.")
    newsletter_heading = models.CharField(max_length=80, default="Stay in touch.")
    newsletter_text = models.CharField(max_length=200, default="Be the first to know about new collections, private events and seasonal edits.")
    footer_note = models.CharField(max_length=160, default="© Favourbrook 2026. All rights reserved.")

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroPanel(models.Model):
    kicker = models.CharField(max_length=80, default="Autumn/Winter '26")
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="home/")
    link = models.CharField(max_length=200)
    button_label = models.CharField(max_length=40, default="Shop Now")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ProductRow(models.Model):
    kicker = models.CharField(max_length=80, blank=True, default="Shop By")
    title = models.CharField(max_length=120)
    collection = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="home_rows")
    button_label = models.CharField(max_length=60, blank=True)
    limit = models.PositiveIntegerField(default=4)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def products(self):
        return self.collection.products.filter(available=True)[:self.limit]


class EditorialCard(models.Model):
    GROUPS = [("editorial", "Editorial"), ("info", "Information")]
    group = models.CharField(max_length=20, choices=GROUPS, default="editorial")
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="home/")
    text = models.TextField(blank=True)
    link = models.CharField(max_length=200)
    button_label = models.CharField(max_length=40, default="Explore")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["group", "order", "id"]

    def __str__(self):
        return self.title


class FeatureBlock(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    image = models.ImageField(upload_to="home/")
    link = models.CharField(max_length=200)
    button_label = models.CharField(max_length=40, default="Shop Now")
    image_right = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class WideHero(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="home/")
    link = models.CharField(max_length=200)
    button_label = models.CharField(max_length=40, default="Explore")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Wide heroes"

    def __str__(self):
        return self.title


class AboutBand(models.Model):
    title = models.CharField(max_length=120, default="Favourbrook")
    text = models.TextField()
    image = models.ImageField(upload_to="home/")

    class Meta:
        verbose_name_plural = "About band"

    def __str__(self):
        return self.title


class UspIcon(models.Model):
    ICONS = [("shipping", "Shipping"), ("globe", "International"), ("store", "Collect in-store"), ("returns", "Returns")]
    icon = models.CharField(max_length=20, choices=ICONS, default="shipping")
    title = models.CharField(max_length=120)
    text = models.CharField(max_length=240)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    intro = models.TextField(blank=True)
    show_in_nav = models.BooleanField(default=False)
    nav_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["nav_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    description = models.TextField(blank=True, help_text="HTML allowed.")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="products/")
    collections = models.ManyToManyField(Category, related_name="products", blank=True)
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def on_sale(self):
        return bool(self.compare_price and self.compare_price > self.price)


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("confirmed", "Confirmed"), ("dispatched", "Dispatched"),
        ("completed", "Completed"), ("cancelled", "Cancelled"),
    ]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=80)
    notes = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} × {self.quantity}"

    @property
    def subtotal(self):
        return (self.price or 0) * (self.quantity or 0)


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%d %b %Y}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Page(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    body = models.TextField(help_text="HTML allowed.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title