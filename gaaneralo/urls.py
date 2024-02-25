
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('category/<slug:category_slug>/',views.home, name='category_wise_post'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('books/', include('books.urls')),
    path('category/', include('category.urls')),
    path('category/', include('transactions.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)