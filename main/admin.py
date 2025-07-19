from django.contrib import admin
from .models import Testimonial, ProductCategory, Product, Program, FAQ, Industry, TeamMember, CompanyInfo, ProgramImage, AccordBusiness, ContactEnquiry, QuoteRequest, JobOpening, AccordGroupInfo, GroupDepartment

class ProgramImageInline(admin.TabularInline):
    model = ProgramImage
    extra = 1

class ProgramAdmin(admin.ModelAdmin):
    inlines = [ProgramImageInline]

class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'product_service', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'company', 'product_service']
    readonly_fields = ['created_at']
    list_per_page = 20

admin.site.register(Testimonial)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ProgramImage)
admin.site.register(FAQ)
admin.site.register(Industry)
admin.site.register(TeamMember)
admin.site.register(CompanyInfo)
admin.site.register(AccordBusiness)
admin.site.register(ContactEnquiry)
admin.site.register(QuoteRequest, QuoteRequestAdmin)
admin.site.register(JobOpening)
admin.site.register(AccordGroupInfo)
admin.site.register(GroupDepartment)
