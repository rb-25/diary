from datetime import date
from diary.core.models import Entry
from diary.users.models import User

def get_users_without_entry(today=date.today()):    
    entries = Entry.objects.filter(created_at__date=today)
    user_ids = entries.values_list('user__id', flat=True)
    return User.objects.exclude(id__in=user_ids)