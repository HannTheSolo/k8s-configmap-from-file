# Python script to create configmap from file.

Pass K8S_API_TOKEN,K8S_API_HOST and K8S_NAMESPACE as an environment variable to the script.

Create ServiceAccount using kubernetes/configmap-role-binding-sa.yaml file, describe secret which it creates and use it for K8S_API_TOKEN value.