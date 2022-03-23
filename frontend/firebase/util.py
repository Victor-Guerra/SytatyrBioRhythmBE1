from google.cloud import storage as gs

# Upload Files to Storage
def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = gs.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Requests the file using the public url
    r = requests.head(blob.public_url)
    # Whether the file exists or not on the server
    fileExists = (r.status_code == requests.codes.ok)
    fileExists = blob.exists()
    if fileExists:
        return 'Image already exists, please change the file name.'

    blob.upload_from_filename(source_file_name)


def get_blob_image(picTemplate, bucket_name):
    storage_client = gs.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(picTemplate)
    url = blob.generate_signed_url(version="v4", expiration=100, method="GET")
    return url