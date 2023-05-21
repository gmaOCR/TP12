# from django.contrib.auth.models import Group
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
#
# @receiver(m2m_changed, sender=Group)
# def update_user_role(sender, instance, action, model, pk_set, **kwargs):
#     if action == 'post_add':
#         group_ids = list(pk_set)
#         if len(group_ids) == 1:
#             group_id = group_ids[0]
#             group = Group.objects.get(pk=group_id)
#             instance.role = group.name
#             instance.save()
