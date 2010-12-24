import urlparse

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from forms import RegistrationForm

@csrf_protect
@never_cache
def signup(request, template_name='registration/signup.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           signup_form=RegistrationForm,
           current_app=None, extra_context=None):
    """
    Displays the signup form and handles the signup action.
    This actually could be nearly identical to the generic login view,
    except it does sign up.
    """

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = signup_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Sign up
            new_user = form.create_user()
            # This is required to set the auth backend.
            new_user = authenticate(username=new_user.username,
                                    password=new_user.password)
            # Log in the user.
            login(request, new_user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = signup_form()

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))


def redirect_to_profile(request):
    return redirect(reverse('profile',
                            kwargs={ 'username': request.user.username }))
