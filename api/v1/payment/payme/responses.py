from api.v1.payment.payme import error_massages


def beautiful_response(
        lang=None, lang_not_found=None, monthly_payment=None, monthly_payment_not_found=None
):
    if lang:return error_massages.MESSAGES['LangMustSend']
    if lang_not_found:return error_massages.MESSAGES['LangNotFound']
    if monthly_payment:return error_massages.MESSAGES['MonthlyPaymentMustSend']
    if monthly_payment_not_found:return error_massages.MESSAGES['MonthlyPaymentNotFound']

