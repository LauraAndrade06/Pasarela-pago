PRODUCT_URLS = {
    'queplan': {
        'qa': 'https://queplan.cl/Comparar/Seguros-de-Salud',
        'staging': 'https://queplan.cl/Compra-Online/CL373',
        'produccion': 'https://queplan.cl/',
        'test': 'https://queplan.cl/Compra-Online/CL373'
    },
    'colsanitas': {
        'qa': 'https://queplan.cl/Comparar/Seguros-de-Salud',
        'staging': 'https://queplan.cl/Compra-Online/CL373',
        'produccion': 'https://queplan.cl/',
        'test': 'https://feature-test2.queplan.cl/Compra-Online/CL534'
    },
    # Agrega más productos aquí
}

def get_product_url(product, environment='qa', tags=None):
    """
    Obtiene la URL del producto según el entorno y los tags de la prueba.
    
    Args:
        product (str): Nombre del producto (ej: 'queplan', 'colsanitas')
        environment (str): Entorno por defecto ('qa', 'staging', 'produccion')
        tags (list): Lista de tags de la prueba (ej: ['featuretest', 'negative'])
        
    Returns:
        str: URL correspondiente al producto y entorno
    """
    # Si hay tag @featuretest, usar siempre el entorno de test
    if tags and 'featuretest' in tags:
        return PRODUCT_URLS.get(product.lower(), {}).get('test')
    
    # Si hay tag @negative, usar siempre el entorno de staging
    elif tags and 'negative' in tags:
        return PRODUCT_URLS.get(product.lower(), {}).get('staging')
    
    # Si hay tag 'produccion', usar el entorno de producción
    elif tags and 'produccion' in tags:
        return PRODUCT_URLS.get(product.lower(), {}).get('produccion')
    
    # Si hay tag 'staging', usar el entorno de staging
    elif tags and 'staging' in tags:
        return PRODUCT_URLS.get(product.lower(), {}).get('staging')
    
    # En cualquier otro caso, usar el entorno proporcionado
    return PRODUCT_URLS.get(product.lower(), {}).get(environment.lower())