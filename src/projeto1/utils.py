import envconfiguration as config

def hostname_from_the_request(request):
    return request.get_host().split(":")[0].lower()


def tenant_db_from_the_request(request):
    hostname = hostname_from_the_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)


def get_tenants_map():
    return {
        f"efg-index.{config.PRIMARY_DOMAIN_NAME}": "efg",  #type: ignore
        f"cotec-index.{config.PRIMARY_DOMAIN_NAME}": "cotec"  # type: ignore
    }
