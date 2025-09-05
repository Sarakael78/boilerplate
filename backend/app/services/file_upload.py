import uuid
from pathlib import Path
from typing import List, Optional

import aiofiles
from fastapi import HTTPException, UploadFile, status
from PIL import Image

from ..core.config import settings


class FileUploadService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR or "uploads")
        self.max_file_size = settings.MAX_FILE_SIZE or 10 * 1024 * 1024  # 10MB
        self.allowed_types = (
            settings.ALLOWED_FILE_TYPES
            or "image/jpeg,image/png,image/gif,application/pdf"
        ).split(",")

        # Create upload directory if it doesn't exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file: UploadFile) -> bool:
        """Validate file size and type."""
        # Check file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {self.max_file_size / (1024*1024)}MB",
            )

        # Check file type
        if file.content_type not in self.allowed_types:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"File type {file.content_type} is not allowed. Allowed types: {', '.join(self.allowed_types)}",
            )

        return True

    def generate_filename(
        self, original_filename: str, user_id: Optional[int] = None
    ) -> str:
        """Generate a unique filename."""
        ext = Path(original_filename).suffix
        unique_id = str(uuid.uuid4())
        user_prefix = f"user_{user_id}_" if user_id else ""
        return f"{user_prefix}{unique_id}{ext}"

    async def save_file(self, file: UploadFile, user_id: Optional[int] = None) -> str:
        """Save uploaded file and return filename."""
        self.validate_file(file)

        filename = self.generate_filename(file.filename, user_id)
        file_path = self.upload_dir / filename

        try:
            # Read file content
            content = await file.read()

            # Validate file size again (in case size wasn't available before)
            if len(content) > self.max_file_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size exceeds maximum allowed size of {self.max_file_size / (1024*1024)}MB",
                )

            # Save file
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)

            return filename

        except Exception as e:
            # Clean up file if it was partially created
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}",
            ) from None

    async def save_image_with_thumbnails(
        self, file: UploadFile, user_id: Optional[int] = None
    ) -> dict:
        """Save image and create thumbnails."""
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="File must be an image",
            )

        # Save original file
        filename = await self.save_file(file, user_id)
        file_path = self.upload_dir / filename

        try:
            # Create thumbnails
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # Create thumbnail sizes
                thumbnails = {}
                sizes = {"small": (150, 150), "medium": (300, 300), "large": (600, 600)}

                for size_name, size in sizes.items():
                    thumb = img.copy()
                    thumb.thumbnail(size, Image.Resampling.LANCZOS)

                    thumb_filename = f"thumb_{size_name}_{filename}"
                    thumb_path = self.upload_dir / thumb_filename

                    thumb.save(thumb_path, "JPEG", quality=85)
                    thumbnails[size_name] = thumb_filename

                return {
                    "original": filename,
                    "thumbnails": thumbnails,
                    "size": img.size,
                    "format": img.format,
                }

        except Exception as e:
            # Clean up files if thumbnail creation failed
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create thumbnails: {str(e)}",
            ) from None

    async def get_file(self, filename: str) -> Optional[Path]:
        """Get file path if it exists."""
        file_path = self.upload_dir / filename
        if file_path.exists() and file_path.is_file():
            return file_path
        return None

    async def delete_file(self, filename: str) -> bool:
        """Delete file and return success status."""
        file_path = self.upload_dir / filename
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    async def delete_user_files(self, user_id: int) -> List[str]:
        """Delete all files belonging to a user."""
        deleted_files = []
        user_prefix = f"user_{user_id}_"

        for file_path in self.upload_dir.glob(f"{user_prefix}*"):
            if file_path.is_file():
                file_path.unlink()
                deleted_files.append(file_path.name)

        return deleted_files

    def get_file_url(self, filename: str) -> str:
        """Get public URL for file."""
        base_url = (
            settings.CDN_URL if settings.CDN_ENABLED else f"{settings.API_V1_STR}/files"
        )
        return f"{base_url}/{filename}"


# Create service instance
file_upload_service = FileUploadService()
