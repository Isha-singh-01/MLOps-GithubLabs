"""
Google Cloud Storage helper functions
"""
from google.cloud import storage
import os
import json

class GCSHelper:
    def __init__(self, bucket_name, credentials_path=None):
        """
        Initialize GCS client
        
        Args:
            bucket_name: Name of the GCS bucket
            credentials_path: Path to service account JSON key (optional)
        """
        if credentials_path and os.path.exists(credentials_path):
            self.client = storage.Client.from_service_account_json(credentials_path)
        else:
            # Use default credentials (works in GitHub Actions)
            self.client = storage.Client()
        
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(self, local_path, gcs_path):
        """
        Upload a file to GCS
        
        Args:
            local_path: Local file path
            gcs_path: Destination path in GCS
        """
        blob = self.bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)
        print(f"Uploaded {local_path} to gs://{self.bucket_name}/{gcs_path}")
        return f"gs://{self.bucket_name}/{gcs_path}"
    
    def download_file(self, gcs_path, local_path):
        """
        Download a file from GCS
        
        Args:
            gcs_path: Source path in GCS
            local_path: Destination local path
        """
        # Ensure local directory exists (only if there's a directory component)
        local_dir = os.path.dirname(local_path)
        if local_dir:  # Only create directory if path contains a directory
            os.makedirs(local_dir, exist_ok=True)
        
        blob = self.bucket.blob(gcs_path)
        
        # Check if blob exists
        if not blob.exists():
            print(f"File not found: gs://{self.bucket_name}/{gcs_path}")
            return False
        
        blob.download_to_filename(local_path)
        print(f"Downloaded gs://{self.bucket_name}/{gcs_path} to {local_path}")
        return True
    
    def file_exists(self, gcs_path):
        """
        Check if a file exists in GCS
        
        Args:
            gcs_path: Path in GCS
        """
        blob = self.bucket.blob(gcs_path)
        return blob.exists()
    
    def list_files(self, prefix=''):
        """
        List files in GCS with given prefix
        
        Args:
            prefix: Path prefix to filter
        """
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
        return [blob.name for blob in blobs]
    
    def delete_file(self, gcs_path):
        """
        Delete a file from GCS
        
        Args:
            gcs_path: Path in GCS
        """
        blob = self.bucket.blob(gcs_path)
        if blob.exists():
            blob.delete()
            print(f"Deleted gs://{self.bucket_name}/{gcs_path}")
        else:
            print(f"File not found, cannot delete: gs://{self.bucket_name}/{gcs_path}")

if __name__ == "__main__":
    # Test GCS operations
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python gcs_helper.py <bucket_name> [credentials_path]")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    credentials_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"\n{'='*60}")
    print(f"Testing GCS Helper")
    print(f"Bucket: {bucket_name}")
    print(f"{'='*60}\n")
    
    try:
        gcs = GCSHelper(bucket_name, credentials_path)
        
        # Test 1: Upload
        print("Test 1: Upload file")
        test_file = 'test.txt'
        with open(test_file, 'w') as f:
            f.write('Hello from GCS!')
        
        gcs.upload_file(test_file, 'test/test.txt')
        print("✅ Upload successful\n")
        
        # Test 2: Check if file exists
        print("Test 2: Check if file exists")
        exists = gcs.file_exists('test/test.txt')
        print(f"File exists: {exists}")
        print("✅ File exists check successful\n")
        
        # Test 3: List files
        print("Test 3: List files")
        files = gcs.list_files('test/')
        print(f"Files in test/: {files}")
        print("✅ List files successful\n")
        
        # Test 4: Download
        print("Test 4: Download file")
        gcs.download_file('test/test.txt', 'downloaded_test.txt')
        
        # Verify download
        with open('downloaded_test.txt', 'r') as f:
            content = f.read()
            print(f"Downloaded content: {content}")
        print("✅ Download successful\n")
        
        # Test 5: Delete
        print("Test 5: Delete file")
        gcs.delete_file('test/test.txt')
        print("✅ Delete successful\n")
        
        # Clean up local files
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists('downloaded_test.txt'):
            os.remove('downloaded_test.txt')
        
        print(f"{'='*60}")
        print("✅ All tests passed!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)