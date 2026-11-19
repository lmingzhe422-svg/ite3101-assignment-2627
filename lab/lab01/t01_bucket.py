import os

from google.cloud import exceptions, storage
from google.oauth2 import service_account

key_file_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'service_account_key.json'))
credentials = service_account.Credentials.from_service_account_file(
    key_file_path)

# Reference to this sample code
# https://cloud.google.com/storage/docs/hosting-static-website#storage-create-bucket-code_samples


def create_static_website_cloud_storage_bucket_if_not_exit(bucket_name: str):
    storage_client = storage.Client(credentials=credentials)
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except exceptions.NotFound:
        bucket = storage_client.create_bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append(
        {"role": "roles/storage.objectViewer", "members": ["allUsers"]})
    bucket.set_iam_policy(policy)
    bucket.configure_website("index.html", "404.html")
    bucket.patch()


def upload_text_to_bucket(bucket_name: str, path_name: str, content: str, content_type: str = "text/html"):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(path_name)
    blob.upload_from_string(content, content_type)


def upload_file_to_bucket(bucket_name: str, path_name: str, source_file_name: str, content_type: str = "image/jpeg"):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(path_name)
    blob.upload_from_filename(source_file_name, content_type=content_type)


def upload_index_and_404_pages(bucket_name: str):
    index = '''
<!DOCTYPE html>
<html>
<head>
<title>Index</title>
</head>
<body>
<h1>Index Page</h1>
</body>
</html>     
'''

    page404 = '''
<!DOCTYPE html>
<html>
<head>
<title>Not Found</title>
</head>
<body>
<h1>Not Found</h1>
</body>
</html>     
'''
    upload_text_to_bucket(bucket_name, "index.html", index)
    upload_text_to_bucket(bucket_name, "404.html", page404)


def upload_html_file_to_bucket(bucket_name: str, path: str, repeat: int):
    for i in range(repeat):
        file_path_name = os.path.join(path, f'{i}.html')
        content = f'''
<!DOCTYPE html>
<html>
<head>
<title>Index</title>
</head>
<body>
<h1>{i}</h1>
</body>
</html>     
'''
        upload_text_to_bucket(bucket_name, file_path_name, content)


def delete_text_html_to_bucket(bucket_name: str, path: str, repeat: int):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    for i in range(repeat):
        file_path_name = os.path.join(path, f'{i}.html')
        blob = bucket.blob(file_path_name)
        if blob.exists():
            blob.delete()  
