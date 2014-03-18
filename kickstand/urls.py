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
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),


)
