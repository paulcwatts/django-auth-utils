from django.contrib.auth.models import User

from django.conf import settings


def is_allowed_username(username):
    disallowed = getattr(settings, 'AUTH_DISALLOWED_USERNAMES', [])
    return username.lower() not in disallowed


def get_username(basename):
    disallowed = getattr(settings, 'AUTH_DISALLOWED_USERNAMES', [])

    # Truncate the basename to 27 characters
    # (The username is only 30 characters)
    basename = basename[:27]
    if basename.lower() not in disallowed:
        try:
            # First just try their username
            User.objects.get(username__iexact=basename)
        except User.DoesNotExist:
            return basename

    i = 0
    while True:
        try:
            username = basename + str(i)
            if username.lower() not in disallowed:
                User.objects.get(username__iexact=username)
            i = i + 1
        except User.DoesNotExist:
            return username


def email_to_username(email):
    # Generate a unique username from the email address
    basename = email.split('@')[0].lower()
    return get_username(basename)
