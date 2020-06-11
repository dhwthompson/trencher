from django.utils import timezone

def date_name(date, today=None):
    if today is None:
        today = timezone.localdate()

    if date is None:
        return ""

    offset_days = (date - today).days
    if offset_days == 0:
        return "Today"
    if offset_days == 1:
        return "Tomorrow"
    if 2 <= offset_days < 7:
        return date.strftime("%A")  # e.g. Monday
    return date.strftime("%A %-d %b")

