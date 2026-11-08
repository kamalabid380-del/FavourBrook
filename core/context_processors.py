from .models import Category, Page, SiteSettings


def site(request):
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())
    return {
        "site": SiteSettings.load(),
        "nav_categories": Category.objects.filter(show_in_nav=True),
        "cart_count": cart_count,
        "footer_pages": Page.objects.all(),
    }