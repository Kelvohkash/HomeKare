from django.db import models
from django.contrib.auth.models import User

class HeroContent(models.Model):
    title = models.CharField(max_length=200, default="Every Home Task Solved in Minutes")
    description = models.TextField(default="Connect with thousands of verified local professionals for repairs, gardening, cleaning, and more. Quality guaranteed.")
    image = models.ImageField(upload_to='hero/', help_text="Worker image for the hero section")

    class Meta:
        verbose_name = "Hero Content"
        verbose_name_plural = "Hero Content"

    def __str__(self):
        return "Hero Section Content"

class Category(models.Model):
    ICON_CHOICES = [
        ('fa-home', 'Home & Household'),
        ('fa-broom', 'Cleaning'),
        ('fa-bug', 'Pest Control'),
        ('fa-truck-moving', 'Movers & Logistics'),
        ('fa-couch', 'Interior Decor'),
        ('fa-car', 'Vehicle Services'),
        ('fa-spa', 'Beauty & Spa'),
        ('fa-cut', 'Barber/Haircut'),
        ('fa-hand-sparkles', 'Manicures'),
        ('fa-magic', 'Makeup'),
        ('fa-wrench', 'Plumbing & Repair'),
        ('fa-bolt', 'Electrical'),
        ('fa-tv', 'Electronics'),
        ('fa-plug', 'Appliances'),
        ('fa-cog', 'Mechanical'),
        ('fa-utensils', 'Catering'),
        ('fa-birthday-cake', 'Pastry'),
        ('fa-calendar-alt', 'Events'),
        ('fa-microphone', 'MC Services'),
        ('fa-camera', 'Photography'),
        ('fa-box', 'Deliveries'),
        ('fa-user-nurse', 'Health & Care'),
        ('fa-shield-alt', 'Security'),
        ('fa-leaf', 'Garden & Landscaping'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, verbose_name="URL Identifier")
    icon = models.CharField(
        max_length=50, 
        choices=ICON_CHOICES,
        default="fa-home", 
        help_text="Select a professional icon for this category"
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Worker(models.Model):
    EXPERIENCE_CHOICES = [
        ('entry', 'Junior (1-2 years)'),
        ('mid', 'Mid-Level (3-5 years)'),
        ('senior', 'Senior (5+ years)'),
        ('master', 'Master Craftsman (10+ years)'),
    ]

    full_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='worker_profile')
    phone_number = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50, unique=True, verbose_name="ID/Passport Number")
    id_scan = models.ImageField(upload_to='workers/ids/', null=True, blank=True, help_text="Upload scan of ID or Passport")
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=200, help_text="Primary area of operation")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='entry')
    skills = models.ManyToManyField(Service, related_name='workers')
    internal_rating = models.FloatField(default=0.0, help_text="Average customer rating (0-5)")
    notes = models.TextField(blank=True, help_text="Internal recruitment and background check notes")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self):
        return f"{self.full_name} ({self.get_experience_level_display()})"

    def update_rating(self):
        from django.db.models import Avg
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.internal_rating = round(float(avg_rating or 0.0), 1)
        self.save(update_fields=['internal_rating'])

class WorkerDocument(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=200, help_text="e.g. Plumbing Certificate")
    file = models.FileField(upload_to='workers/docs/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} - {self.worker.full_name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Response'),
        ('matching', 'Finding Worker'),
        ('assigned', 'Worker Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    contact_preference = models.CharField(max_length=10, choices=[('email', 'Email'), ('phone', 'Phone')], default='email')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price agreed upon before assignment")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service.title} - {self.customer_name} ({self.status})"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    checkout_request_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    transaction_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pay {self.transaction_code} - {self.amount}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.worker.full_name} ({self.rating} stars)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.worker.update_rating()

    def delete(self, *args, **kwargs):
        worker = self.worker
        super().delete(*args, **kwargs)
        worker.update_rating()

class UserProfile(models.Model):
    CONTACT_PREFERENCE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call/SMS'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    contact_preference = models.CharField(max_length=10, choices=CONTACT_PREFERENCE_CHOICES, default='email')
    
    def __str__(self):
        return f"Profile for {self.user.email}"
