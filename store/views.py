from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from category.models import Category
from store.models import Color, Product, ProductGallery, Size


def productlist(products):
    product1 = []
    for single_product in products:
        product1.append({
            'id': single_product.id,
            'product_name': single_product.product_name,
            'slug': single_product.slug,
            'descrbtion': single_product.descrbtion,
            'price': single_product.price,
            'image': single_product.image,
            'stock': single_product.stock,
            'offer': single_product.offer,
            'is_available': single_product.is_available,
            'category': single_product.category,
            'created_date': single_product.created_date,
            'modified_date': single_product.modified_date,
            'offer_product': (single_product.price - (single_product.price * single_product.category.offer) / 100)-(single_product.price - (single_product.price * single_product.category.offer)/100 * single_product.offer)/100,
        })
    return product1


def store(request, category_slug=None, color_slug=None, size_slug=None):

    categories = None
    products = None
    if category_slug != None:
        try:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(
                category__in=Category.objects.get(
                    category_name=category_slug).get_descendants(include_self=True)
            )
            # products = Product.objects.filter(
            #     category__in=Category.objects.get(
            #         name=category_slug).get_descendants(include_self=True), is_available=True)
            product1 = productlist(products)
            paginator = Paginator(product1, 8)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        except Exception as e:
            return redirect('store:storehome')
    elif color_slug != None:
        color = get_object_or_404(Color, slug=color_slug)
        try:
            products = Product.objects.all().filter(
                variations__variation_value=color.name).order_by('id')
            product1 = productlist(products)
            paginator = Paginator(product1, 8)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        except Exception as e:
            return redirect('store:storehome')
    elif size_slug != None:
        size = get_object_or_404(Size, slug=size_slug)
        try:
            products = Product.objects.all().filter(
                variations__variation_value=size.name).order_by('id')
            product1 = productlist(products)
            paginator = Paginator(product1, 8)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        except Exception as e:
            return redirect('store:storehome')
    else:

        ordering = request.GET.get('ordering', "")
        price = request.GET.get('price', "")
        products = Product.objects.all().filter(is_available=True).order_by('id')
        if ordering:
            products = products.order_by(ordering)
        if price:
            products = products.filter(price__lt=price)
        product1 = productlist(products)
        paginator = Paginator(product1, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, product_slug, category_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        # get the product gallery
        product_gallery = ProductGallery.objects.filter(
            product_id=single_product.id)
        product_offer = (single_product.price - (single_product.price * single_product.category.offer) / 100)-(
            single_product.price - (single_product.price * single_product.category.offer)/100 * single_product.offer)/100,
        # wishlist = WishlistItem.objects.all()
        context = {
            'single_product': single_product,
            'product_offer': product_offer[0],
            'product_gallery': product_gallery,
            # 'wishlist': wishlist,
        }
        if request.GET.get('color'):
            color_ = request.GET.get('color')
            price = single_product.get_price_by_colors(color_)
            single_product.price = price
            context['selected_color']=color_
            context['single_product'] = single_product
            update_price = (price - (price * single_product.category.offer) / 100)-(
            price - (price * single_product.category.offer)/100 * single_product.offer)/100
            print(update_price)
            context['update_price'] = update_price

    except Exception as e:
        raise e

    return render(request, 'store/product_detail.html', context)


# search function

def search(request):
    print(101)
    # print(request.GET["keyword"])
    try:
        if "keyword" in request.GET:
            print(102)
            keyword = request.GET["keyword"]
            if keyword:
                products = Product.objects.order_by("-created_date").filter(
                    Q(descrbtion__icontains=keyword) | Q(product_name__icontains=keyword))
                product_count = products.count()
            product1 = productlist(products)
            context = {
                'products': product1,
                'product_count': product_count,
            }
        return render(request, 'store/store.html', context)
    except Exception as e:
        return redirect('store:storehome')


def suggestionApi(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(
            product_name__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.product_name)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request, 'core/home.html')
