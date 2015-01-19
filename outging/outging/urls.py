from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()
import xadmin
xadmin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'outging.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^', include('main.urls')),
)
