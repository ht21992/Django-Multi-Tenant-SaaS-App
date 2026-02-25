from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from products.models import Product

# Create your views here.


def index_view(request):
    products = Product.objects.filter(is_active=True)  # Only show active products
    context = {
        "products": products,
    }
    return render(request, "tenant/index.html", context=context)


def create_product_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        product_type = request.POST.get("type")
        price = request.POST.get("price")
        is_active = (
            request.POST.get("is_active") == "on"
        )  # Checkbox returns "on" when checked

        product = Product.objects.create(
            name=name,
            description=description,
            type=product_type,
            price=price,
            is_active=is_active,
        )

        # Format the date in Python
        created_date = product.created_at.strftime("%B %d, %Y")

        # Determine badge colors based on values
        active_badge_class = (
            "bg-green-100 text-green-800"
            if product.is_active
            else "bg-gray-100 text-gray-800"
        )
        active_text = "Active" if product.is_active else "Inactive"

        type_badge_class = (
            "bg-blue-100 text-blue-800"
            if product.type == "product"
            else "bg-purple-100 text-purple-800"
        )
        type_display = dict(Product.PRODUCT_TYPE)[product.type]

        # Build the description HTML if description exists
        description_html = (
            f'<p class="mt-3 text-lg text-gray-500 leading-relaxed max-w-2xl">{product.description}</p>'
            if product.description
            else ""
        )

        html = f"""<li class="border-b border-gray-200 pb-8">
                    <div class="flex justify-between items-start">
                        <h2 class="text-5xl font-thin tracking-tight">
                            { product.name }
                        </h2>
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium {active_badge_class}">
                            {active_text}
                        </span>
                    </div>

                    <div class="mt-2 flex items-center gap-4 flex-wrap">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {type_badge_class}">
                            {type_display}
                        </span>
                        <span class="text-2xl font-semibold text-gray-900">
                            ${product.price}
                        </span>
                    </div>

                    {description_html}

                    <div class="mt-4 text-sm text-gray-400">
                        Added: {created_date}
                    </div>
                </li>"""
        return HttpResponse(html, status=201)
    return redirect("home")
