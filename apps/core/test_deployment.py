from types import SimpleNamespace
from unittest.mock import Mock

from django.core.files.base import ContentFile
from django.test import SimpleTestCase

from tsavo_hub.storage import VercelBlobStorage


class VercelBlobStorageTests(SimpleTestCase):
    def setUp(self):
        self.storage = VercelBlobStorage()
        self.storage._client = Mock()

    def test_save_returns_persistent_public_blob_url(self):
        blob_url = "https://example.public.blob.vercel-storage.com/team/photo-abc.jpg"
        self.storage.client.put_blob.return_value = SimpleNamespace(url=blob_url)

        saved_name = self.storage._save("team/photo.jpg", ContentFile(b"image-bytes"))

        self.assertEqual(saved_name, blob_url)
        self.assertEqual(self.storage.url(saved_name), blob_url)
        _, payload = self.storage.client.put_blob.call_args.args
        self.assertEqual(payload, b"image-bytes")
        self.assertEqual(self.storage.client.put_blob.call_args.kwargs["access"], "public")
        self.assertTrue(self.storage.client.put_blob.call_args.kwargs["add_random_suffix"])

    def test_delete_uses_stored_blob_url(self):
        blob_url = "https://example.public.blob.vercel-storage.com/team/photo-abc.jpg"
        self.storage.delete(blob_url)
        self.storage.client.delete_blob.assert_called_once_with(blob_url)
