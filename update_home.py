import os

filepath = "/home/ktb/restaurants/restaurants/users/views/home_view.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace(
    "from restaurants.meal.models import Meal, Boisson, DailyMenu",
    "from restaurants.meal.models import Meal, Boisson, DailyMenu, Category"
)

old_meals_query = """        context['meals'] = Meal.objects.filter(is_available=True).annotate(
            is_today=Exists(
                DailyMenu.objects.filter(
                    day=today_day,
                    is_active=True,
                    meals=OuterRef('pk')
                )
            )
        ).order_by('-is_today', 'category__display_order', 'name').select_related('category')"""

new_meals_query = """        context['meals'] = Meal.objects.filter(is_available=True).annotate(
            is_today=Exists(
                DailyMenu.objects.filter(
                    day=today_day,
                    is_active=True,
                    meals=OuterRef('pk')
                )
            )
        ).order_by('-is_today', 'category__display_order', 'name').select_related('category').prefetch_related('daily_menus')"""

content = content.replace(old_meals_query.replace("\n", "").replace(" ", ""), new_meals_query.replace("\n", "").replace(" ", ""))

# The formatting might be weird because of the newlines, let's just do a simpler replacement or use python re.
