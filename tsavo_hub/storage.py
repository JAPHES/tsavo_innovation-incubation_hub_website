"""Persistent media storage for deployments using Vercel Blob."""

import mimetypes
from pathlib import PurePosixPath
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class VercelBlobStorage(Storage):
    """Store public, administrator-uploaded website images in Vercel Blob."""

    access = "public"

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from django.conf import settings
            from vercel.blob import sync

            if not settings.BLOB_READ_WRITE_TOKEN:
                raise ImproperlyConfigured(
                    "BLOB_READ_WRITE_TOKEN is required for Vercel Blob storage."
                )
            self._client = sync
        return self._client

    @staticmethod
    def _is_blob_url(name):
        parsed = urlparse(str(name))
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

    def _save(self, name, content):
        pathname = str(PurePosixPath(name.replace("\\", "/")))
        content_type = (
            getattr(content, "content_type", None)
            or mimetypes.guess_type(pathname)[0]
            or "application/octet-stream"
        )
        payload = b"".join(content.chunks())
        uploaded = self.client.put_blob(
            pathname,
            payload,
            access=self.access,
            add_random_suffix=True,
            content_type=content_type,
        )
        return uploaded.url

    def _open(self, name, mode="rb"):
        if mode not in {"r", "rb"}:
            raise ValueError("Vercel Blob media can only be opened for reading.")
        blob_url = self.url(name)
        data = self.client.get_blob(blob_url, access=self.access).body
        filename = PurePosixPath(urlparse(blob_url).path).name
        return ContentFile(data, name=filename)

    def delete(self, name):
        if name:
            self.client.delete_blob(name)

    def exists(self, name):
        if not name or not self._is_blob_url(name):
            return False
        from vercel.blob.errors import BlobNotFoundError

        try:
            self.client.head_blob(name)
        except BlobNotFoundError:
            return False
        return True

    def size(self, name):
        return self.client.head_blob(name).size

    def get_modified_time(self, name):
        return self.client.head_blob(name).uploaded_at

    def url(self, name):
        if self._is_blob_url(name):
            return str(name)
        return self.client.head_blob(name).url
