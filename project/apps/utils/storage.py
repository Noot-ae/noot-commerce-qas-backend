from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.deconstruct import deconstructible

@deconstructible
class MyStorage(S3Boto3Storage):
    folder_prefix = "ecommerce-media"
    host = "https://noot-ae.s3.me-central-1.amazonaws.com"
    
    def get_available_name(self, name, max_length=None):
        """
        Get the available name for the file, adding the base_path if provided.
        """
        name = f"{self.folder_prefix}/{name}"
        return super().get_available_name(name, max_length)
    
    def url(self, name : str):
        if name is None: return
        if name.startswith(self.folder_prefix):                
            return f"{self.host}/{name}"
        else:
            return f"{self.host}/{self.folder_prefix}/{name}"
        
        