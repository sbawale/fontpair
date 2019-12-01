from django.shortcuts import render

# Create your views here.
# *********** CATEGORIES ***********
def categories(request):
    categories = Category.objects.all().order_by('category_name')
    context = {
        'categories': categories
    }
    return render(request, 'categories.html', context)

def font_category(request, category):
    fonts = Font.objects.filter(
        categories__name__contains=category).order_by('name')
    context = {
        "category": category,
        "fonts": fonts
    }
    return render(request, "font_category.html", context)