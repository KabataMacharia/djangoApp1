from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def staff_member_required(view_func=None, redirect_field_name='not_allowed',
                          login_url='not_allowed'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def admin_member_required(view_func=None, redirect_field_name="not_allowed",
                          login_url='not_allowed'):
    """
    Decorator for views that checks that the user is logged in and is an admin
    member, redirecting if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def superuser_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='not_allowed'):
    """
    Decorator for views that checks that the user is logged in and is a superuser
    member, redirecting if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def staff_superuser_not_allowed(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='not_allowed'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_superuser and not u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator