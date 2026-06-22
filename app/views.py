from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Blog, Skill, Experience, FAQ, Resume, ContactMessage
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.http import JsonResponse
from django.http import FileResponse, HttpResponse
import logging
from django.utils import timezone


logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def handle_contact_submission(request):
    """Handle contact form submission and save to database with rate limiting"""
    try:
        # Rate Limiting: Max 3 requests per IP per day
        client_ip = get_client_ip(request)
        today = timezone.now() - timezone.timedelta(days=1)
        recent_submissions = ContactMessage.objects.filter(
            subject__endswith=f"[{client_ip}]", 
            created_at__gte=today
        ).count()
        
        if recent_submissions >= 3:
            return JsonResponse({
                "success": False, 
                "error": "You have reached the maximum number of contact requests for today. Please try again tomorrow."
            }, status=429)

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        # Validate required fields
        if not all([name, email, subject, message]):
            return JsonResponse({
                "success": False, 
                "error": "All fields are required"
            }, status=400)

        # Save to database (append IP to subject for tracking)
        contact_message = ContactMessage.objects.create(
            name=name[:100],  # Hard limit size to prevent DB truncation errors
            email=email[:254],
            subject=f"{subject[:150]} [{client_ip}]",
            message=message[:5000] # Max 5000 chars
        )

        # Try to send email (optional, won't fail if email doesn't work)
        try:
            send_mail(
                subject=f"New Contact Form: {subject}",
                message=f"From: {name} ({email})\n\nMessage:\n{message}",
                from_email="contact@roshandamor.site",
                recipient_list=["contact@roshandamor.site"],
                fail_silently=True,
            )
            logger.info(f"Email sent successfully for contact ID: {contact_message.id}")
        except Exception as email_error:
            logger.warning(f"Email sending failed but contact saved: {email_error}")

        return JsonResponse({
            "success": True,
            "message": "Your message has been sent successfully! We'll get back to you soon."
        })
        
    except Exception as e:
        logger.error(f"Contact form submission failed: {e}")
        return JsonResponse({
            "success": False, 
            "error": "Something went wrong. Please try again later."
        }, status=500)

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        logger.info(f"Received data: Name={name}, Email={email}, Message={message}")

        if not all([name, email, message]):
            logger.error("Form data missing")
            return JsonResponse({"success": False, "error": "Missing fields"}, status=400)

        try:
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=f"Sender: {name}\nEmail: {email}\nMessage: {message}",
                from_email="contact@roshandamor.site",
                recipient_list=["contact@roshandamor.site"],
                fail_silently=False,
            )
            logger.info("Email sent successfully")
            return JsonResponse({"success": True})
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def latest_resume(request):
    latest_resume = Resume.objects.order_by("-uploaded_at").first()
    return {"resume": latest_resume}
    
def get_resume(request):
    latest_resume = Resume.objects.order_by("-uploaded_at").first()
    if latest_resume:
        return FileResponse(
            latest_resume.file.open(),
            content_type='application/pdf',
            headers={'Content-Disposition': 'inline; filename="resume.pdf"'}
        )
    return HttpResponse("No resume found", status=404)

def download_resume(request):
    latest_resume = Resume.objects.order_by("-uploaded_at").first()
    
    if latest_resume and latest_resume.file: 
        latest_resume.file.open() 
        response = FileResponse(latest_resume.file, as_attachment=True, filename=latest_resume.file.name)
        return response

    return HttpResponse("No resume available", status=404)

def user_terms_view(request):
    return render(request, "user-terms.html")

def get_unique_categories(queryset, field_name):
    """Extract unique categories from a given model field optimally."""
    categories = set()
    # Fetch only the non-empty categories strings directly from DB
    raw_cats = queryset.exclude(**{f"{field_name}__isnull": True}).exclude(**{f"{field_name}__exact": ""}).values_list(field_name, flat=True)
    for obj in raw_cats:
        for cat in obj.split(","):
            clean_cat = cat.strip()
            if clean_cat and clean_cat.lower() != "uncategorized":
                categories.add(clean_cat)
    return sorted(categories)

def home(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return handle_contact_submission(request)
    
    sort_by = request.GET.get("sort", "-publication_date")  
    category = request.GET.get("category", "")

    # Optimized prefetching
    projects = Project.objects.prefetch_related("images", "skills").all()
    blogs = Blog.objects.all()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    faqs = FAQ.objects.all()

    if category:
        projects = projects.filter(categories__icontains=category)
        blogs = blogs.filter(categories__icontains=category)
        skills = skills.filter(categories__icontains=category)
        experiences = experiences.filter(categories__icontains=category)
        faqs = faqs.filter(categories__icontains=category)

    projects = projects.order_by(sort_by)[:3]
    blogs = blogs.order_by(sort_by)[:3]
    skills = skills.order_by("-level")[:6]
    experiences = experiences.order_by("-start_date")[:3]
    faqs = faqs.order_by("-created_at")[:5]

    blog_categories = get_unique_categories(Blog.objects, "categories")
    project_categories = get_unique_categories(Project.objects, "categories")
    faq_categories = get_unique_categories(FAQ.objects, "categories")
    skill_categories = get_unique_categories(Skill.objects, "categories")
    experience_categories = get_unique_categories(Experience.objects, "categories")

    return render(request, "portfolio-landing-page.html", {
        "projects": projects,
        "blogs": blogs,
        "skills": skills,
        "experiences": experiences,
        "faqs": faqs,
        "selected_category": category,
        "selected_sort": sort_by,
        "blog_categories": blog_categories,
        "project_categories": project_categories,
        "faq_categories": faq_categories,
        "skill_categories": skill_categories,
        "experience_categories": experience_categories,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('images', 'features', 'learnings', 'skills'), slug=slug)

    category_list = project.get_category_list()
    similar_projects = Project.objects.prefetch_related("images", "skills").filter(
        categories__iregex=r'(' + '|'.join(category_list) + ')'
    ).exclude(id=project.id)[:3]

    latest_projects = Project.objects.prefetch_related("images", "skills").exclude(id=project.id).order_by('-created_at')[:3]

    return render(request, 'project-detail.html', {
        'project': project,
        'similar_projects': similar_projects,
        'latest_projects': latest_projects
    })

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    category_list = [cat.strip() for cat in blog.categories.split(",") if cat.strip()]
    similar_blogs = Blog.objects.filter(
        categories__iregex=r'(' + '|'.join(category_list) + ')'
    ).exclude(id=blog.id)[:3]

    latest_blogs = Blog.objects.exclude(id=blog.id).order_by('-created_at')[:3]

    return render(request, 'blog-detail.html', {
        'blog': blog,
        'similar_blogs': similar_blogs,
        'latest_blogs': latest_blogs
    })


# Project Views
def project_list(request):
    query = request.GET.get('search', '')  
    category = request.GET.get('category', '')  
    sort_by = request.GET.get('sort', 'latest')  

    projects = Project.objects.prefetch_related('images', 'skills').all()
    category_list = get_unique_categories(Project.objects, "categories")

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(categories__icontains=query)
        ).distinct()

    if category and category != "all":  
        projects = projects.filter(categories__icontains=category)

    if sort_by == 'oldest':
        projects = projects.order_by('created_at')
    else:  # latest
        projects = projects.order_by('-created_at')

    # Pagination: 6 per page
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'projects.html', {
        'projects': page_obj, 
        'page_obj': page_obj,
        'query': query, 
        'selected_category': category, 
        'sort': sort_by, 
        'category_list': category_list
    })


# Blog Views
def blog_list(request):
    query = request.GET.get('search', '')  
    category = request.GET.get('category', '')  
    sort_by = request.GET.get('sort', 'latest')  

    blogs = Blog.objects.all()
    category_list = get_unique_categories(Blog.objects, "categories")

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(categories__icontains=query)
        ).distinct()

    if category and category != "all":  
        blogs = blogs.filter(categories__icontains=category)

    if sort_by == 'oldest':
        blogs = blogs.order_by('publication_date')
    else:  # latest
        blogs = blogs.order_by('-publication_date')

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogs.html', {
        'blogs': page_obj, 
        'page_obj': page_obj,
        'query': query, 
        'selected_category': category, 
        'sort': sort_by, 
        'category_list': category_list
    })


# Skill Views
def skill_list(request):
    query = request.GET.get('search', '')  
    category = request.GET.get('category', '')  
    sort_by = request.GET.get('sort', 'latest')  

    skills = Skill.objects.all()
    category_list = get_unique_categories(Skill.objects, "categories")

    if query:
        skills = skills.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(categories__icontains=query)
        ).distinct()

    if category and category != "all":  
        skills = skills.filter(categories__icontains=category)

    if sort_by == 'oldest':
        skills = skills.order_by('created_at')
    elif sort_by == 'level':
        skills = skills.order_by('-level')  
    elif sort_by == 'name':
        skills = skills.order_by('name')
    else:  # latest
        skills = skills.order_by('-created_at')

    paginator = Paginator(skills, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'skills.html', {
        'skills': page_obj, 
        'page_obj': page_obj,
        'query': query, 
        'selected_category': category, 
        'sort': sort_by, 
        'category_list': category_list
    })


# Experience Views
def experience_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '-start_date')  

    experiences = Experience.objects.all()
    category_list = get_unique_categories(Experience.objects, "categories")

    if query:
        experiences = experiences.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(categories__icontains=query)
        ).distinct()

    if category and category != "all":  
        experiences = experiences.filter(categories__icontains=category)

    if sort_by == 'oldest':
        experiences = experiences.order_by('start_date')
    else:
        experiences = experiences.order_by('-start_date')

    paginator = Paginator(experiences, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'experiences.html', {
        'experiences': page_obj, 
        'page_obj': page_obj,
        'query': query, 
        'category': category, 
        'sort_by': sort_by, 
        'categories': category_list
    })


# FAQs View
def faq_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'latest')

    faqs = FAQ.objects.all()
    
    # FAQ uses 'categories' now to match others based on models.py
    category_list = get_unique_categories(FAQ.objects, "categories")

    if query:
        faqs = faqs.filter(
            Q(question__icontains=query) | 
            Q(answer__icontains=query) |
            Q(categories__icontains=query)
        ).distinct()

    if category and category != "all":  
        faqs = faqs.filter(categories__icontains=category)

    if sort_by == 'oldest':
        faqs = faqs.order_by('created_at')
    else:  # latest
        faqs = faqs.order_by('-created_at')

    paginator = Paginator(faqs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'faqs.html', {
        'faqs': page_obj, 
        'page_obj': page_obj,
        'query': query, 
        'selected_category': category, 
        'sort': sort_by, 
        'category_list': category_list
    })
