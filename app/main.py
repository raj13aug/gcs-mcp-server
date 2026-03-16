# server.py
import os
import logging
from fastmcp import FastMCP
from google.cloud import storage

# Initialize FastMCP
mcp = FastMCP("gcs-mcp-server")

# Initialize GCS Client
storage_client = storage.Client()

@mcp.tool()
def list_buckets() -> str:
    """Lists all Google Cloud Storage buckets in the project."""
    buckets = list(storage_client.list_buckets())
    return "\n".join([bucket.name for bucket in buckets])

@mcp.tool()
def create_bucket(bucket_name: str, location: str = "US") -> str:
    """Creates a new GCS bucket."""
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location=location)
    return f"Created bucket {new_bucket.name} in {location}"

@mcp.tool()
def delete_bucket(bucket_name: str) -> str:
    """
    Deletes a GCS bucket. 
    WARNING: This forces deletion of all objects and versions inside.
    """
    bucket = storage_client.bucket(bucket_name)
    
    # Robust cleanup: List and delete all blob versions to avoid "Bucket not empty" errors
    blobs = list(storage_client.list_blobs(bucket_name, versions=True))
    for blob in blobs:
        blob.delete()
        
    bucket.delete(force=True)
    return f"Deleted bucket {bucket_name}"

if __name__ == "__main__":
    # DUAL MODE LOGIC
    if "PORT" in os.environ:
        # We are in Cloud Run -> Start an SSE Server
        import uvicorn
        port = int(os.environ["PORT"])
        print(f"Starting SSE server on port {port}...")
        
        # Critical for Cloud Run: Allow proxy headers and bind to 0.0.0.0
        uvicorn.run(
            mcp._sse_app, 
            host="0.0.0.0", 
            port=port, 
            proxy_headers=True, 
            forwarded_allow_ips='*',
            timeout_keep_alive=300 # Prevent SSE connection drops
        )
    else:
        # We are local -> Start Stdio Server
        mcp.run()