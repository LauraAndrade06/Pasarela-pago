PRODUCT_URLS = {
    'queplan': {
        'qa': 'https://feature-test2.queplan.cl/Compra-Online/CL534',
        'staging': 'https://staging.queplan.cl/Compra-Online/CL534',

    },
    'colsanitas': {
        'qa': 'https://feature-test2.queplan.cl/Compra-Online/CL534',
        'staging': 'https://staging.queplan.cl/Compra-Online/CL534',

    },
    # Agrega más productos aquí
}

def get_product_url(product, environment='qa'):
    return PRODUCT_URLS.get(product.lower(), {}).get(environment.lower())