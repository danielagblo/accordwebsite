from django.shortcuts import render, get_object_or_404
from .models import CompanyInfo, TeamMember, Program, ProductCategory, Product, Industry, FAQ, Testimonial, JobOpening, AccordBusiness, ContactEnquiry
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Create your views here.

def home(request):
    from .models import CompanyInfo, TeamMember, Testimonial
    company_info = CompanyInfo.objects.first()
    team = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    # Placeholder data if empty
    if not company_info:
        class Placeholder:
            about = "Accord Industrial Services is a leading provider of high-quality personal protective equipment (PPE) and safety solutions for industries worldwide. Our commitment to safety, innovation, and reliability has made us a trusted partner for businesses of all sizes."
            mission = "To protect and empower workers everywhere by delivering the best PPE and safety solutions."
            values = "Integrity, Innovation, Customer Focus, Safety First, Sustainability."
            connection_to_accord = "A proud member of the Accord Group, connecting safety and excellence across industries."
        company_info = Placeholder()
    if not team:
        class T:
            def __init__(self, name, role, bio, photo):
                self.name = name
                self.role = role
                self.bio = bio
                self.photo = photo
        team = [
            T("Alex Morgan", "Chief Executive Officer", "Alex brings 20+ years of industrial safety leadership and a passion for innovation.", "https://randomuser.me/api/portraits/men/11.jpg"),
            T("Priya Patel", "Head of Operations", "Priya ensures seamless delivery and top-notch service for all our clients.", "https://randomuser.me/api/portraits/women/21.jpg"),
            T("James Lee", "Lead Safety Engineer", "James is dedicated to developing and implementing the latest in PPE technology.", "https://randomuser.me/api/portraits/men/31.jpg"),
        ]
    return render(request, 'home.html', {
        'company_info': company_info,
        'team': team,
        'testimonials': testimonials,
    })

def about(request):
    company_info = CompanyInfo.objects.first()
    team = TeamMember.objects.all()
    return render(request, 'about.html', {
        'company_info': company_info,
        'team': team,
    })

def programs(request):
    programs = Program.objects.prefetch_related('images').all()
    if not programs:
        class P:
            def __init__(self, title, description):
                self.title = title
                self.description = description
        programs = [
            P("Safety Awareness Campaigns", "Ongoing campaigns to promote workplace safety and PPE best practices across industries."),
            P("PPE Donation Initiatives", "We partner with NGOs to donate PPE to communities and frontline workers in need."),
            P("Industry Partnerships", "Collaborating with leading companies to raise safety standards and share knowledge."),
            P("Training Sessions & Workshops", "Hands-on training and workshops to ensure proper PPE usage and compliance."),
        ]
    return render(request, 'programs.html', {'programs': programs})

def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    industries = Industry.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        products = [p for p in products if (getattr(p, 'category', None) and (getattr(p.category, 'name', None) == selected_category))]
    if not categories:
        class C:
            def __init__(self, name):
                self.name = name
        categories = [C("Head Protection"), C("Hand Protection"), C("Eye Protection"), C("Respiratory Protection"), C("Body Protection")]
    if not products:
        class Prod:
            def __init__(self, category, name, description, certifications, image):
                self.category = category
                self.name = name
                self.description = description
                self.certifications = certifications
                self.image = image
        products = [
            Prod(categories[0], "Hard Hat", "Durable, lightweight hard hat for head protection.", "ANSI Z89.1, CE EN397", "https://images.unsplash.com/photo-1517971071642-34a2d3eccb5e?auto=format&fit=crop&w=400&q=80"),
            Prod(categories[1], "Nitrile Gloves", "Chemical-resistant gloves for hand safety.", "EN374, FDA", "https://images.unsplash.com/photo-1588776814546-ec7e8c1b1b1b?auto=format&fit=crop&w=400&q=80"),
            Prod(categories[2], "Safety Goggles", "Anti-fog, impact-resistant goggles for eye protection.", "ANSI Z87.1, CE EN166", "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=400&q=80"),
            Prod(categories[3], "Respirator Mask", "Reusable respirator mask for dust and fumes.", "NIOSH, CE EN140", "https://images.unsplash.com/photo-1588776814546-ec7e8c1b1b1b?auto=format&fit=crop&w=400&q=80"),
            Prod(categories[4], "High-Visibility Vest", "Reflective vest for body protection in low-light environments.", "ANSI/ISEA 107, CE EN ISO 20471", "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=400&q=80"),
        ]
        if selected_category:
            products = [p for p in products if (getattr(p, 'category', None) and (getattr(p.category, 'name', None) == selected_category))]
    if not industries:
        class Ind:
            def __init__(self, name, description, icon):
                self.name = name
                self.description = description
                self.icon = icon
        industries = [
            Ind("Construction", "Safety solutions for construction sites and workers.", "https://cdn-icons-png.flaticon.com/512/2965/2965567.png"),
            Ind("Manufacturing", "PPE for factories, plants, and industrial manufacturing.", "https://cdn-icons-png.flaticon.com/512/2965/2965562.png"),
            Ind("Healthcare", "Medical-grade PPE for healthcare professionals.", "https://cdn-icons-png.flaticon.com/512/2965/2965565.png"),
            Ind("Mining, Oil & Gas", "Specialized protection for hazardous environments.", "https://cdn-icons-png.flaticon.com/512/2965/2965570.png"),
            Ind("Logistics & Warehousing", "Safety gear for logistics, transport, and warehousing.", "https://cdn-icons-png.flaticon.com/512/2965/2965569.png"),
        ]
    return render(request, 'products.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'industries': industries,
    })

def industries(request):
    industries = Industry.objects.all()
    if not industries:
        class Ind:
            def __init__(self, name, description, icon):
                self.name = name
                self.description = description
                self.icon = icon
        industries = [
            Ind("Construction", "Safety solutions for construction sites and workers.", "https://cdn-icons-png.flaticon.com/512/2965/2965567.png"),
            Ind("Manufacturing", "PPE for factories, plants, and industrial manufacturing.", "https://cdn-icons-png.flaticon.com/512/2965/2965562.png"),
            Ind("Healthcare", "Medical-grade PPE for healthcare professionals.", "https://cdn-icons-png.flaticon.com/512/2965/2965565.png"),
            Ind("Mining, Oil & Gas", "Specialized protection for hazardous environments.", "https://cdn-icons-png.flaticon.com/512/2965/2965570.png"),
            Ind("Logistics & Warehousing", "Safety gear for logistics, transport, and warehousing.", "https://cdn-icons-png.flaticon.com/512/2965/2965569.png"),
        ]
    return render(request, 'industries.html', {'industries': industries})

def faqs(request):
    faqs = FAQ.objects.all()
    if not faqs:
        class F:
            def __init__(self, question, answer):
                self.question = question
                self.answer = answer
        faqs = [
            F("Do you offer bulk order options?", "Yes, we provide special pricing and logistics for bulk and corporate orders."),
            F("Are your products certified?", "All our PPE products meet or exceed international safety standards and certifications."),
            F("What are your delivery timelines?", "Standard delivery is 3-5 business days. Express options are available."),
            F("How can I partner with Accord?", "Contact us via the inquiry form or email to discuss partnership opportunities."),
            F("What payment methods do you accept?", "We accept bank transfer, credit card, and corporate invoicing."),
        ]
    return render(request, 'faqs.html', {'faqs': faqs})

def testimonials(request):
    testimonials = Testimonial.objects.all()
    if not testimonials:
        class T:
            def __init__(self, client_name, company, content, logo, video):
                self.client_name = client_name
                self.company = company
                self.content = content
                self.logo = logo
                self.video = video
        testimonials = [
            T("Emily Carter", "GlobalBuild", "Accord's PPEs are reliable and always delivered on time. Our team's safety has never been better!", None, None),
            T("Michael Brown", "HealthFirst", "The quality and comfort of Accord's products are unmatched. Highly recommended!", None, None),
            T("Fatima Al-Sayed", "SafeMines", "Their donation initiative made a real difference for our workers.", None, None),
        ]
    return render(request, 'testimonials.html', {'testimonials': testimonials})

def accord_group(request):
    company_info = CompanyInfo.objects.first()
    team = TeamMember.objects.all()
    businesses = AccordBusiness.objects.all()
    return render(request, 'accord_group.html', {
        'company_info': company_info,
        'team': team,
        'businesses': businesses,
    })

def contact(request):
    company_info = CompanyInfo.objects.first()
    jobs = JobOpening.objects.all()
    faqs = FAQ.objects.all()
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        if name and email and message:
            ContactEnquiry.objects.create(name=name, email=email, phone=phone, message=message)
            success = True
    if not company_info:
        class Placeholder:
            contact_email = "info@accordindustrialsafety.com"
            contact_phone = "0303959251, 0209136429, 0548210788, 0502226144"
            office_location = "Off shalom spot on the lashibi road,beside my kids college-Towards the comm. 18 Roundabout"
            map_embed = '<iframe src="https://www.openstreetmap.org/export/embed.html?bbox=-0.128590,51.507351,-0.127758,51.507351&amp;layer=mapnik" style="border:1px solid black;width:100%;height:250px;"></iframe>'
        company_info = Placeholder()
    if not jobs:
        class J:
            def __init__(self, title, description, location, posted_at):
                self.title = title
                self.description = description
                self.location = location
                self.posted_at = posted_at
        jobs = [
            J("Sales Executive", "Drive B2B sales and build relationships with industrial clients.", "Remote / USA", "2024-06-01"),
            J("Warehouse Supervisor", "Oversee warehouse operations and ensure safety compliance.", "Logistics Park, USA", "2024-05-20"),
        ]
    if not faqs:
        class F:
            def __init__(self, question, answer):
                self.question = question
                self.answer = answer
        faqs = [
            F("Do you offer bulk order options?", "Yes, we provide special pricing and logistics for bulk and corporate orders."),
            F("Are your products certified?", "All our PPE products meet or exceed international safety standards and certifications."),
            F("What are your delivery timelines?", "Standard delivery is 3-5 business days. Express options are available."),
            F("How can I partner with Accord?", "Contact us via the inquiry form or email to discuss partnership opportunities."),
            F("What payment methods do you accept?", "We accept bank transfer, credit card, and corporate invoicing."),
        ]
    return render(request, 'contact.html', {
        'company_info': company_info,
        'jobs': jobs,
        'faqs': faqs,
        'success': success,
    })

def program_detail(request, pk):
    program = get_object_or_404(Program.objects.prefetch_related('images'), pk=pk)
    other_programs = Program.objects.exclude(pk=pk)
    return render(request, 'program_detail.html', {
        'program': program,
        'other_programs': other_programs,
    })

def download_catalog(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_catalog.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 1 * inch

    p.setFont("Helvetica-Bold", 18)
    p.drawString(1 * inch, y, "Product Catalog")
    y -= 0.5 * inch

    p.setFont("Helvetica", 12)
    products = Product.objects.select_related('category').all()
    for product in products:
        if y < 1 * inch:
            p.showPage()
            y = height - 1 * inch
            p.setFont("Helvetica", 12)
        p.drawString(1 * inch, y, f"Name: {product.name}")
        y -= 0.25 * inch
        p.drawString(1.2 * inch, y, f"Category: {product.category.name if product.category else ''}")
        y -= 0.25 * inch
        p.drawString(1.2 * inch, y, f"Details: {product.description}")
        y -= 0.4 * inch
    p.save()
    return response
