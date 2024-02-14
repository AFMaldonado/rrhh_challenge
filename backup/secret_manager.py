from google.cloud import secretmanager

class SecretManagerGCP:
    def __init__(self, project_id):
        """
        Initializes an instance of SecretManager.

        Args:
            project_id (str): GCP project ID where secrets will be stored.
        """
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, name_secret):
        """
        Retrieves the latest version of the specified secret from Secret Manager.

        Args:
            name_secret (str): The name of the secret to retrieve.

        Returns:
            str: The value of the retrieved secret.
        
        Raises:
            Exception: If an error occurs while loading the secret.
        """
        resource_name = f"projects/{self.project_id}/secrets/{name_secret}/versions/latest"

        try:
            response = self.client.access_secret_version(name=resource_name)
            payload = response.payload.data.decode("UTF-8")
            return payload
        except Exception as e:
            raise Exception(f"Error loading the secret: {str(e)}")
