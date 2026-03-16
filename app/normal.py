import os
import asyncio
from fastmcp import FastMCP
from google.cloud import storage

# Initialize MCP server
mcp = FastMCP("gcs-mcp-server")

# Initialize GCS client
storage_client = storage.Client()


@mcp.tool()
async def list_gcs_buckets():
    """
    List all Google Cloud Storage buckets in the current project.
    """
    buckets = storage_client.list_buckets()
    return [bucket.name for bucket in buckets]


@mcp.tool()
async def create_bucket(bucket_name: str):
    """
    Create a new Google Cloud Storage bucket.
    """
    bucket = storage_client.create_bucket(bucket_name)
    return f"Bucket {bucket.name} created successfully."


@mcp.tool()
async def delete_bucket(bucket_name: str):
    """
    Delete a Google Cloud Storage bucket.
    """
    bucket = storage_client.bucket(bucket_name)
    bucket.delete()
    return f"Bucket {bucket_name} deleted successfully."


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )