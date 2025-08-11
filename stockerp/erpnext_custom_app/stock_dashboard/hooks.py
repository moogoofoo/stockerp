

from frappe import _

def get_context(context):
    context.no_cache = 1

def get_list_context(context):
    context.add_button = {
        'label': _('View Dashboard'),
        'url': '/stock_dashboard',
        'class': 'btn-primary'
    }

