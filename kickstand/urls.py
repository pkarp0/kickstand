from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from kickstand.views import HomePageView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kickstand.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^/?$', 'jqm.views.home', name='home'),
    url(r'^register/$', 'jqm.views.register', name='register'),
    url(r'^register/success/$', 'jqm.views.register_success'),

    url(r'^place/(?P<id>\d+)/$', 'places.views.detail', name='place-detail'),
    url(r'^add_nearby/$', 'places.views.add_nearby', name='add_nearby'),
    url(r'^nearby/$', 'places.views.nearby', name='nearby'),

    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^accounts/login/$','django.contrib.auth.views.login',
        dict(
            template_name = 'jqm/login.html',
        ),
        name='login',
    ),
    url(
        r'^accounts/logout/$','django.contrib.auth.views.logout',
        dict(
            template_name = 'jqm/logout.html',
        ),
        name='logout',
    ),


)
