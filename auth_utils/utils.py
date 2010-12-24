from django.contrib.auth.models import User

def _get_username(basename):
    try:
        # First just try their username
        User.objects.get(username=basename)
    except User.DoesNotExist:
        return basename

    i=0
    while True:
        try:
            username=basename+str(i)
            User.objects.get(username=username)
            i = i + 1
        except User.DoesNotExist:
            return username

def email_to_username(email):
    # Generate a unique username from the email address
    basename = email.split('@')[0].lower()
    return _get_username(basename)

