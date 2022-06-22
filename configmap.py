from kubernetes import client, config
import kubernetes
import sys
import os


configuration = kubernetes.client.Configuration()
configuration.api_key['authorization'] = os.getenv('K8S_API_TOKEN')
configuration.api_key_prefix['authorization'] = 'Bearer'
configuration.host = os.getenv('K8S_API_HOST')
configuration.verify_ssl = False
# configuration.debug = True

with kubernetes.client.ApiClient(configuration) as api_client:

    api_core_client = kubernetes.client.CoreV1Api(api_client)

    html_file = open('index.html')
    html_file_data = html_file.read()
    configmap_name = 'angular-index-html-cmap'
    namespace = os.getenv('K8S_NAMESPACE')

    api_list = api_core_client.list_namespaced_config_map(namespace=namespace)

    config_map_data = client.V1ConfigMap()
    config_map_data.data = {}
    config_map_data.metadata = client.V1ObjectMeta(name=configmap_name)
    config_map_data.data["index.html"] = f"{html_file_data}"

    returned_configmap_names = []

    for items in api_list.items:
        returned_configmap_names.append(items.metadata.name)

    if configmap_name in returned_configmap_names:

        print(f'ConfigMap {configmap_name} Found! Patching it with new version')

        api_patch = api_core_client.patch_namespaced_config_map(namespace=namespace, body=config_map_data,
                                                                name=configmap_name)
    else:

        print(f'No configmap found with the name {configmap_name} ! Creating ...')

        api_create = api_core_client.create_namespaced_config_map(namespace=namespace, body=config_map_data)

sys.exit(0)
