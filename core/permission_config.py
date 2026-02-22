from product.models import Product

PERMISSION_CONFIG = {
    'customer': {
        Product: ['view'],
        # Order: ['']
    },
    'seller': {
        Product: ['view', 'add', 'change'],
        # Order: ['']
    }
}