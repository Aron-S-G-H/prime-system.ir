from django.shortcuts import render
from django.views.generic import View
from hitcount.views import HitCountDetailView
from .models import BlogPost, BlogTag, BlogCategory, BlogComment
from django.core.paginator import Paginator
from django.http import JsonResponse


class BlogListView(View):
    def get(self, request):
        tag_slug = request.GET.get('tag', None)
        category_slug = request.GET.get('category', None)
        page_number = request.GET.get('page', None)
        if tag_slug:
            blogs = BlogPost.objects.filter(publish=True, tags__slug=tag_slug).select_related('author', 'category').defer('tags', 'description')
        elif category_slug:
            blogs = BlogPost.objects.filter(publish=True, category__slug=category_slug).select_related('author', 'category').defer('tags', 'description')
        else:
            blogs = BlogPost.objects.filter(publish=True).select_related('author', 'category').defer('tags', 'description')
        if not blogs:
            return render(request, 'blog_app/no-blog.html')
        blog_categories = BlogCategory.objects.all()
        blog_tags = BlogTag.objects.all()
        paginator = Paginator(blogs, 9)
        blogs_list = paginator.get_page(page_number)
        context = {'blog_list': blogs_list, 'blog_tags': blog_tags, 'blog_categories': blog_categories}
        return render(request, 'blog_app/blog.html', context)


class BlogDetailView(HitCountDetailView):
    model = BlogPost
    context_object_name = 'blog'
    template_name = 'blog_app/blog-detail.html'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_slug = self.kwargs.get('slug')
        related_blogs = BlogPost.objects.filter(publish=True).exclude(slug=blog_slug).select_related('category').defer('author', 'tags', 'description', 'introduction')[:5]
        context['related_blogs'] = related_blogs
        context['range'] = range(1, 6)
        return context

    # Post Method is for Creating Comments
    def post(self, request, slug):
        try:
            blog = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return JsonResponse({'status': 400, 'error_message': 'خطا در دریافت مقاله مربوطه'})

        text = request.POST.get('text').strip()
        rating = int(request.POST.get('rating'))
        parent_id = request.POST.get('parent_id')

        if not text:
            return JsonResponse({'status': 400, 'error_message': 'متن نظر الزامی است'})
        if not (0 <= rating <= 5):
            return JsonResponse({'status': 400, 'error_message': 'مقدار امتیاز باید بین ۰ و ۵ باشد'})

        BlogComment.objects.create(blog=blog, parent_id=parent_id, user=request.user, text=text, rating=rating)
        return JsonResponse({'status': 200})
