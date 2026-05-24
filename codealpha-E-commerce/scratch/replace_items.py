import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from shop.models import Product, Category

# Get the category
try:
    home_living = Category.objects.get(slug='home-living')
    
    # Replace Washing Machine
    Product.objects.filter(name='LG Front Load Washing Machine').update(
        name='Dyson V15 Detect Vacuum',
        slug='dyson-v15-detect-vacuum',
        price=749.99,
        description='The most powerful, intelligent cordless vacuum. Laser reveals microscopic dust.',
        image='products/2026/05/05/dyson_v15.jpg'
    )
    
    # Replace Steam Iron
    Product.objects.filter(name='Professional Steam Iron').update(
        name='KitchenAid Artisan Stand Mixer',
        slug='kitchenaid-artisan-stand-mixer',
        price=449.99,
        description='Iconic design with 10 speeds and over 10 available attachments. Perfect for every baking need.',
        image='products/2026/05/05/kitchenaid_mixer.jpg'
    )
    
    print("Successfully replaced items in the database.")
except Exception as e:
    print(f"Error: {e}")
