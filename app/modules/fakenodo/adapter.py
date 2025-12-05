"""
FakenodoAdapter - Configurable adapter for Fakenodo service

Configures behavior based on FAKENODO_URL environment variable:
- If set to HTTP URL → uses remote HTTP API
- If not set → uses local FakenodoService (database-backed mock)

This allows seamless switching between local mock and external service.
"""
import os
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class FakenodoAdapter:
    """Adapter that routes operations to either remote Fakenodo HTTP API
    or local DB-backed FakenodoService based on FAKENODO_URL env var.
    """

    def __init__(self):
        self.base_url = os.getenv("FAKENODO_URL")
        self._service = None
        self.is_remote = bool(self.base_url and str(self.base_url).startswith("http"))
        
        # Aumentar timeout para localhost (puede ser el mismo servidor)
        self.timeout = 60 if "localhost" in str(self.base_url) else 30
        
        if self.is_remote:
            logger.info(f"FakenodoAdapter: Using REMOTE service at {self.base_url}")
            logger.info(f"  Timeout: {self.timeout}s")
        else:
            logger.info("FakenodoAdapter: Using LOCAL FakenodoService")

    def _get_service(self):
        """Lazy import of local service to avoid circular imports"""
        if not self._service:
            from app.modules.fakenodo.services import FakenodoService
            self._service = FakenodoService()
        return self._service

    def create_fakenodo(self, dataset) -> dict:
        """Create a new Fakenodo deposition record.
        
        Args:
            dataset: MovieDataset object with ds_meta_data and user_id
            
        Returns:
            dict: {
                "id": fakenodo_id,
                "deposition_id": deposition_id,
                "fakenodo_doi": doi or None,
                "dataset_metadata": metadata dict,
                "status": "draft" or other status
            }
        """
        if self.is_remote:
            url = f"{self.base_url.rstrip('/')}/fakenodo/create"
            payload = {
                "metadata_id": dataset.ds_meta_data_id,
                "user_id": dataset.user_id,
                "dataset_type": "movie"
            }
            try:
                logger.info(f"Calling remote Fakenodo: POST {url}")
                resp = requests.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                
                # Adapt remote response to expected format
                return {
                    "id": data.get("fakenodo_id"),
                    "deposition_id": data.get("fakenodo_id"),
                    "fakenodo_doi": data.get("fakenodo_response", {}).get("fakenodo_doi"),
                    "dataset_metadata": dataset.ds_meta_data.to_dict(),
                    "status": data.get("fakenodo_response", {}).get("status", "draft")
                }
            except requests.Timeout as e:
                logger.error(f"Timeout calling remote Fakenodo (waited {self.timeout}s)")
                logger.error("Possible causes:")
                logger.error("  1. FAKENODO_URL points to the same Flask server (circular call)")
                logger.error("  2. Flask not running with --threaded or --with-threads")
                logger.error("  3. Remote service is actually down")
                logger.error("Solution: Run Fakenodo on different port or unset FAKENODO_URL")
                raise Exception(f"Fakenodo timeout after {self.timeout}s - check logs")
            except requests.RequestException as e:
                logger.exception(f"Error calling remote Fakenodo create: {e}")
                raise Exception(f"Failed to create remote Fakenodo: {str(e)}")
        else:
            svc = self._get_service()
            return svc.create_fakenodo(dataset)

    def upload_file_to_fakenodo(
        self, 
        fakenodo_id: int, 
        file_content: bytes, 
        filename: str, 
        dataset_id: int
    ) -> dict:
        """Upload a file to Fakenodo storage.
        
        Args:
            fakenodo_id: ID of the Fakenodo record
            file_content: Binary file content
            filename: Original filename
            dataset_id: Dataset ID for organization
            
        Returns:
            dict: {
                "fakenodo_id": int,
                "dataset_id": int,
                "file_path": str,
                "checksum": str,
                "status": str
            }
        """
        if self.is_remote:
            url = f"{self.base_url.rstrip('/')}/fakenodo/upload/{fakenodo_id}"
            files = {"file": (filename, file_content)}
            data = {
                "dataset_id": dataset_id,
                "filename": filename
            }
            try:
                logger.info(f"Uploading file to remote Fakenodo: POST {url}")
                resp = requests.post(url, files=files, data=data, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                logger.exception(f"Error uploading file to remote Fakenodo: {e}")
                raise Exception(f"Failed to upload file: {str(e)}")
        else:
            svc = self._get_service()
            return svc.upload_file_to_fakenodo(
                fakenodo_id=fakenodo_id,
                file_content=file_content,
                filename=filename,
                dataset_id=dataset_id
            )

    def publish_fakenodo(self, fakenodo_id: int):
        """Publish a Fakenodo deposition and generate DOI.
        
        Args:
            fakenodo_id: ID of the Fakenodo record to publish
            
        Returns:
            Fakenodo object (local) or dict (remote) with status and doi
        """
        if self.is_remote:
            url = f"{self.base_url.rstrip('/')}/fakenodo/publish/{fakenodo_id}"
            try:
                resp = requests.post(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                logger.exception(f"Error publishing remote Fakenodo: {e}")
                raise Exception(f"Failed to publish Fakenodo: {str(e)}")
        else:
            svc = self._get_service()
            return svc.publish_fakenodo(fakenodo_id)

    def get_fakenodo(self, fakenodo_id: int) -> dict:
        """Get Fakenodo deposition information.
        
        Args:
            fakenodo_id: ID of the Fakenodo record
            
        Returns:
            dict: {
                "fakenodo_doi": str or None,
                "deposition_id": int,
                "dataset_metadata": dict,
                "status": str,
                "minor_change_logs": list
            }
        """
        if self.is_remote:
            url = f"{self.base_url.rstrip('/')}/fakenodo/{fakenodo_id}"
            try:
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                logger.exception(f"Error getting remote Fakenodo: {e}")
                raise Exception(f"Failed to get Fakenodo: {str(e)}")
        else:
            svc = self._get_service()
            return svc.get_fakenodo(fakenodo_id)

    def get_doi_versions(self, fakenodo_id: int) -> dict:
        """Get available versions for a Fakenodo record.
        
        Args:
            fakenodo_id: ID of the Fakenodo record
            
        Returns:
            dict: {
                "version-list": str representation,
                "current-version": str,
                "doi": str
            }
        """
        if self.is_remote:
            url = f"{self.base_url.rstrip('/')}/fakenodo/{fakenodo_id}/versions"
            try:
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                logger.exception(f"Error getting remote versions: {e}")
                raise Exception(f"Failed to get versions: {str(e)}")
        else:
            svc = self._get_service()
            return svc.get_doi_versions(fakenodo_id)

    def get_doi(self, fakenodo_id: int) -> Optional[str]:
        """Get the DOI of a published Fakenodo record.
        
        Args:
            fakenodo_id: ID of the Fakenodo record
            
        Returns:
            str: DOI string or None if not published
        """
        try:
            data = self.get_fakenodo(fakenodo_id)
            return data.get("fakenodo_doi") or data.get("doi")
        except Exception as e:
            logger.warning(f"Could not retrieve DOI for fakenodo {fakenodo_id}: {e}")
            return None