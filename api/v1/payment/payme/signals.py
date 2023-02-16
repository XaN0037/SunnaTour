from api.v1.payment.payme.models import MerchatTransactionsModel
from bmain.models import PaymentCourseTransaction
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=MerchatTransactionsModel)
def contract_signals(sender, instance, created, **kwargs):
    with open("logs.txt", "a") as file:
        file.write(f"sender {sender} tr_id {instance.transaction_id} created: {created} kwargs: {kwargs}")

    if created:
        order_id = instance.order_id
        payme_course_transaction = PaymentCourseTransaction.objects.select_related('transaction', 'user', 'order').get(
            order_id=order_id
        )
        payme_course_transaction.is_payed = True
        payme_course_transaction.save()


@receiver(post_save, sender=PaymentCourseTransaction)
def contract_signals(sender, instance, created, **kwargs):
    if created:
        instance.payed_amount = str(instance.monthly_plan.monthly_price)
        instance.save()
