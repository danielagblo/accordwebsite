from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    logo = models.ImageField(upload_to='testimonials/logos/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client_name} - {self.company}"

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    certifications = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Program(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.title

class ProgramImage(models.Model):
    program = models.ForeignKey(Program, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='programs/', blank=False, null=False)
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.program.title}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question

class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='industries/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class CompanyInfo(models.Model):
    about = models.TextField()
    mission = models.TextField()
    vision = models.TextField(blank=True, null=True)
    values = models.TextField()
    connection_to_accord = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=50, blank=True)
    office_location = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=255, blank=True)
    map_embed = models.TextField(blank=True)
    
    def __str__(self):
        return "Company Info"

class JobOpening(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    posted_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class AccordBusiness(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='businesses/', blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class ContactEnquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at:%Y-%m-%d %H:%M}"

class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=100, blank=True)
    product_service = models.CharField(max_length=200, help_text="Product or service you're interested in")
    quantity = models.CharField(max_length=50, blank=True, help_text="Quantity needed")
    requirements = models.TextField(blank=True, help_text="Additional requirements or specifications")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('quoted', 'Quoted'),
        ('closed', 'Closed')
    ], default='pending')

    def __str__(self):
        return f"{self.name} - {self.product_service} ({self.created_at:%Y-%m-%d})"

    class Meta:
        ordering = ['-created_at']

@receiver(post_save, sender=QuoteRequest)
def send_quote_notification(sender, instance, created, **kwargs):
    if created:  # Only send email for new quote requests
        subject = f'New Quote Request from {instance.name}'
        message = f"""
New quote request received:

Name: {instance.name}
Email: {instance.email}
Phone: {instance.phone}
Company: {instance.company}
Product/Service: {instance.product_service}
Quantity: {instance.quantity}
Requirements: {instance.requirements}
Date: {instance.created_at}

You can view this request in the admin panel.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email notification: {e}")
