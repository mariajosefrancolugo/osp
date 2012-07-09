from osp.core.models import StudentIndex

def update_index(sender, instance, signal, **kwargs):
    """Update the student index on user save"""
    if instance.groups.filter(name='Students'):
        si, new = StudentIndex.objects.get_or_create(student=instance)

        si.first_name = instance.first_name
        si.last_name = instance.last_name
        si.full_name = instance.get_full_name()
        si.email = instance.email
        si.id_number = instance.profile.id_number

        si.save()
