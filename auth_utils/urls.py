from django.conf.urls.defaults import *
from django.contrib.auth import views as auth

urlpatterns = patterns('',
    url(r'^signup/$', 'auth_utils.views.signup', name='account_signup'),

    # Auth urls
    url(r'^signin/$',
        auth.login,
        name='account_signin'),
    url(r'^signout/$',
        auth.logout,
        name='account_signout'),
    url(r'^password/change/$',
        auth.password_change,
        name='account_passwordchange'),
    url(r'^password/change/done/$',
        auth.password_change_done,
        name='account_passwordchangedone'),
    url(r'^password/reset/$',
        auth.password_reset,
        name='account_passwordreset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth.password_reset_confirm,
        name='account_passwordresetconfirm'),
    url(r'^password/reset/complete/$',
        auth.password_reset_complete,
        name='account_passwordresetcomplete'),
    url(r'^password/reset/done/$',
        auth.password_reset_done,
        name='account_passwordresetdone')
)
