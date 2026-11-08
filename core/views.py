from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, ContactForm
from .models import (
    AboutBand, Category, EditorialCard, FeatureBlock, HeroPanel,
    NewsletterSubscriber, Order, OrderItem, Page, Product, ProductRow,
    SiteSettings, UspIcon, WideHero,
)


def home(request):
    context = {
        "panels": HeroPanel.objects.filter(is_active=True),
        "rows": ProductRow.objects.filter(is_active=True).select_related("collection"),
        "editorials": EditorialCard.objects.filter(is_active=True, group="editorial"),
        "info_cards": EditorialCard.objects.filter(is_active=True, group="info"),
        "feature": FeatureBlock.objects.filter(is_active=True).first(),
        "wide_hero": WideHero.objects.filter(is_active=True).first(),
        "about": AboutBand.objects.first(),
        "usps": UspIcon.objects.all(),
    }
    return render(request, "core/home.html", context)


def _sorted(products, sort):
    if sort == "price-asc":
        return products.order_by("price", "id")
    if sort == "price-desc":
        return products.order_by("-price", "id")
    if sort == "name":
        return products.order_by("name", "id")
    return products.order_by("order", "id")


def collection(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = _sorted(category.products.filter(available=True), request.GET.get("sort", ""))
    return render(request, "core/collection.html", {
        "category": category,
        "products": products,
        "sort": request.GET.get("sort", ""),
        "count": products.count(),
    })


def catalog(request):
    products = _sorted(Product.objects.filter(available=True), request.GET.get("sort", ""))
    return render(request, "core/collection.html", {
        "category": None,
        "page_title": "Shop All",
        "products": products,
        "sort": request.GET.get("sort", ""),
        "count": products.count(),
    })


def search(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.filter(available=True)
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    products = _sorted(products, request.GET.get("sort", ""))
    return render(request, "core/collection.html", {
        "category": None,
        "page_title": f"Search: {q}" if q else "Search",
        "query": q,
        "products": products,
        "sort": request.GET.get("sort", ""),
        "count": products.count(),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    first_collection = product.collections.first()
    more = Product.objects.none()
    if first_collection:
        more = first_collection.products.filter(available=True).exclude(pk=product.pk).distinct()[:4]
    return render(request, "core/product.html", {"product": product, "more": more})


def page(request, slug):
    obj = get_object_or_404(Page, slug=slug)
    return render(request, "core/page.html", {"page": obj})


def _cart(request):
    return request.session.get("cart", {})


def _cart_lines(request):
    cart = _cart(request)
    lines, total = [], Decimal("0.00")
    products = Product.objects.in_bulk([int(k) for k in cart.keys()])
    for key, qty in list(cart.items()):
        product = products.get(int(key))
        if not product:
            del cart[key]
            continue
        subtotal = product.price * qty
        total += subtotal
        lines.append({"product": product, "quantity": qty, "subtotal": subtotal})
    request.session["cart"] = cart
    return lines, total


def _safe_next(request, fallback):
    nxt = request.POST.get("next") or request.GET.get("next") or ""
    if nxt.startswith("/") and not nxt.startswith("//"):
        return nxt
    return fallback


def cart_detail(request):
    lines, total = _cart_lines(request)
    return render(request, "core/cart.html", {"lines": lines, "total": total})


@require_POST
def cart_add(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if not product.available:
        messages.error(request, "This piece is currently sold out.")
        return redirect("product_detail", slug=slug)
    try:
        qty = max(1, min(20, int(request.POST.get("quantity", 1))))
    except (TypeError, ValueError):
        qty = 1
    cart = _cart(request)
    cart[str(product.pk)] = cart.get(str(product.pk), 0) + qty
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your basket.")
    return redirect(_safe_next(request, "cart_detail"))


@require_POST
def cart_update(request, pk):
    cart = _cart(request)
    key = str(pk)
    if key in cart:
        try:
            qty = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            qty = 1
        if qty <= 0:
            del cart[key]
        else:
            cart[key] = min(20, qty)
        request.session["cart"] = cart
    return redirect("cart_detail")


@require_POST
def cart_remove(request, pk):
    cart = _cart(request)
    cart.pop(str(pk), None)
    request.session["cart"] = cart
    return redirect("cart_detail")


def checkout(request):
    lines, total = _cart_lines(request)
    if not lines:
        messages.info(request, "Your basket is empty.")
        return redirect("catalog")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total = total
            order.save()
            for line in lines:
                OrderItem.objects.create(
                    order=order, product=line["product"], name=line["product"].name,
                    price=line["product"].price, quantity=line["quantity"],
                )
            request.session["cart"] = {}
            return redirect("order_success", pk=order.pk)
    else:
        form = CheckoutForm()
    return render(request, "core/checkout.html", {"form": form, "lines": lines, "total": total})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "core/order_success.html", {"order": order})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — our team will be in touch shortly.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


@require_POST
def newsletter(request):
    email = request.POST.get("email", "").strip()
    if email:
        NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(request, "You're subscribed. Welcome to Favourbrook.")
    return redirect(_safe_next(request, "home"))


def robots(request):
    body = "\n".join([
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /basket/",
        "Disallow: /checkout/",
        "Disallow: /search/",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ])
    return HttpResponse(body, content_type="text/plain")


def sitemap(request):
    paths = [reverse("home"), reverse("catalog"), reverse("contact")]
    paths += [reverse("collection", args=[c.slug]) for c in Category.objects.all()]
    paths += [reverse("product_detail", args=[p.slug]) for p in Product.objects.filter(available=True)]
    paths += [reverse("page", args=[p.slug]) for p in Page.objects.all()]
    entries = "".join(
        f"<url><loc>{escape(request.build_absolute_uri(path))}</loc></url>" for path in paths
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
    return HttpResponse(xml, content_type="application/xml")