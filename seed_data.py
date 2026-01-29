import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtaani_project.settings')
django.setup()

from web.models import Category, Service, Worker, HeroContent

def seed_data():
    print("Starting data seeding...")

    # 1. Update Hero Content if exists
    hero = HeroContent.objects.first()
    if hero:
        hero.title = "Every Home Task <br> <span class='gradient-text'>Solved in Minutes</span>"
        hero.description = "Connect with thousands of verified local workers for repairs, gardening, cleaning, and more. Quality guaranteed."
        hero.save()
        print("Updated Hero Content.")

    # 2. Create Categories
    # Based on USER_REQUEST
    categories_data = [
        {'name': 'Home & Household Services', 'slug': 'home-household', 'icon': 'fa-home'},
        {'name': 'Pest Control & Fumigation', 'slug': 'pest-control', 'icon': 'fa-bug'},
        {'name': 'Beauty, Grooming & Personal Care', 'slug': 'beauty-grooming', 'icon': 'fa-spa'},
        {'name': 'Repairs, Maintenance & Technical', 'slug': 'repairs-technical', 'icon': 'fa-wrench'},
        {'name': 'Events, Hospitality & Creative', 'slug': 'events-creative', 'icon': 'fa-utensils'},
        {'name': 'Logistics & Delivery', 'slug': 'logistics', 'icon': 'fa-box'},
        {'name': 'Health & Care Services', 'slug': 'health-care', 'icon': 'fa-user-nurse'},
        {'name': 'Security & Safety', 'slug': 'security', 'icon': 'fa-shield-alt'},
    ]

    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name'], 'icon': cat_data['icon']}
        )
        if not created:
            cat.name = cat_data['name']
            cat.icon = cat_data['icon']
            cat.save()
        categories[cat_data['slug']] = cat
        print(f"{'Created' if created else 'Updated'} category: {cat.name}")

    # 3. Create Services
    services_data = [
        # Home & Household
        {'title': 'Mama Fua (Laundry)', 'category': 'home-household', 'price': 800, 'desc': 'Professional washing, drying, and folding of clothes and linens.'},
        {'title': 'General House Cleaners', 'category': 'home-household', 'price': 1500, 'desc': 'Comprehensive house cleaning for a spotless home.'},
        {'title': 'Landscaping & Gardening', 'category': 'home-household', 'price': 2500, 'desc': 'Beautifying your outdoor space with pruning and flower care.'},
        
        # Pest Control & Fumigation
        {'title': 'Pest Control Services', 'category': 'pest-control', 'price': 3000, 'desc': 'Safe and effective elimination of cockroaches, bedbugs, and ants.'},
        {'title': 'Professional Movers', 'category': 'pest-control', 'price': 10000, 'desc': 'Hassle-free household moving and shifting services.'},
        {'title': 'Interior Decor & Curtains', 'category': 'pest-control', 'price': 5000, 'desc': 'Expert interior styling and custom curtain installation.'},
        {'title': 'Mobile Car Wash', 'category': 'pest-control', 'price': 1000, 'desc': 'Professional vehicle wash and detailing at your doorstep.'},

        # Beauty & Grooming
        {'title': 'Salon Services', 'category': 'beauty-grooming', 'price': 2000, 'desc': 'Hair braiding, styling, and restorative treatments.'},
        {'title': 'Kinyozi (Barber)', 'category': 'beauty-grooming', 'price': 500, 'desc': 'Modern haircuts and facial grooming for men.'},
        {'title': 'Manicure & Pedicure', 'category': 'beauty-grooming', 'price': 1200, 'desc': 'Pampering nail care and foot therapy.'},
        {'title': 'Makeup Services', 'category': 'beauty-grooming', 'price': 3500, 'desc': 'Glamorous makeup for weddings, photoshoots, and events.'},

        # Repairs & Technical
        {'title': 'Plumbing Services', 'category': 'repairs-technical', 'price': 1500, 'desc': 'Fixing leaks, blockages, and new pipe installations.'},
        {'title': 'Electrical Services', 'category': 'repairs-technical', 'price': 2000, 'desc': 'Wiring, lighting fixes, and safety inspections.'},
        {'title': 'Electronics Repair', 'category': 'repairs-technical', 'price': 2500, 'desc': 'Expert repair for TVs, computers, and sound systems.'},
        {'title': 'Home Appliances Repair', 'category': 'repairs-technical', 'price': 3000, 'desc': 'Fixing fridges, washing machines, and ovens.'},
        {'title': 'Mechanical Services', 'category': 'repairs-technical', 'price': 4000, 'desc': 'On-call maintenance for generators and basic machinery.'},

        # Events & Creative
        {'title': 'Catering Services', 'category': 'events-creative', 'price': 15000, 'desc': 'Delicious meals prepared for any occasion or event.'},
        {'title': 'Pastry Services', 'category': 'events-creative', 'price': 3000, 'desc': 'Custom cakes and pastries for celebrations.'},
        {'title': 'Event Planners', 'category': 'events-creative', 'price': 20000, 'desc': 'Full-scale coordination for weddings and parties.'},
        {'title': 'MC Services', 'category': 'events-creative', 'price': 10000, 'desc': 'Energetic and professional masters of ceremony.'},
        {'title': 'Photography & Videography', 'category': 'events-creative', 'price': 15000, 'desc': 'Capturing your special moments in high definition.'},

        # Logistics
        {'title': 'Package Deliveries', 'category': 'logistics', 'price': 300, 'desc': 'Fast and secure delivery of small parcels within the city.'},

        # Health
        {'title': 'Nurses and Caregivers', 'category': 'health-care', 'price': 5000, 'desc': 'Compassionate home nursing and elderly care.'},

        # Security
        {'title': 'Security Services', 'category': 'security', 'price': 8000, 'desc': 'Vetted guards and security consulting for your peace of mind.'},
    ]

    for s_data in services_data:
        service, created = Service.objects.get_or_create(
            title=s_data['title'],
            defaults={
                'category': categories[s_data['category']],
                'price': Decimal(s_data['price']),
                'description': s_data['desc']
            }
        )
        if not created:
            service.category = categories[s_data['category']]
            service.price = Decimal(s_data['price'])
            service.description = s_data['desc']
            service.save()
        print(f"{'Created' if created else 'Updated'} service: {service.title}")

    print("Data seeding completed successfully!")

if __name__ == '__main__':
    seed_data()
