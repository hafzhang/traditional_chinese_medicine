"""
CDN Service
CDN视频服务层 - MVP
支持阿里云OSS (Aliyun OSS)
"""

from typing import Optional
import os
from pathlib import Path

from api.config import settings

try:
    import oss2
    OSS2_AVAILABLE = True
except ImportError:
    OSS2_AVAILABLE = False

try:
    from qcloud_cos import CosConfig, CosS3Client
    COS_AVAILABLE = True
except ImportError:
    COS_AVAILABLE = False


class CDNService:
    """CDN服务类 - 统一的CDN接口"""

    def __init__(self, provider: str = "aliyun"):
        """
        初始化CDN服务

        Args:
            provider: CDN提供商 ("aliyun" 或 "tencent")
        """
        self.provider = provider

        if provider == "aliyun" and OSS2_AVAILABLE:
            self._init_aliyun_oss()
        elif provider == "tencent" and COS_AVAILABLE:
            self._init_tencent_cos()
        else:
            self.client = None

    def _init_aliyun_oss(self):
        """初始化阿里云OSS"""
        if not settings.OSS_ACCESS_KEY_ID or not settings.OSS_ACCESS_KEY_SECRET:
            print("Warning: OSS credentials not configured")
            self.client = None
            return

        auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
        self.client = oss2.Bucket(
            auth,
            settings.OSS_ENDPOINT,
            settings.OSS_BUCKET_NAME
        )
        self.base_url = f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}"

    def _init_tencent_cos(self):
        """初始化腾讯云COS"""
        if not settings.TENCENT_COS_SECRET_ID or not settings.TENCENT_COS_SECRET_KEY:
            print("Warning: Tencent COS credentials not configured")
            self.client = None
            return

        config = CosConfig(
            Region=settings.TENCENT_COS_REGION,
            SecretId=settings.TENCENT_COS_SECRET_ID,
            SecretKey=settings.TENCENT_COS_SECRET_KEY
        )
        self.client = CosS3Client(config)
        self.base_url = f"https://{settings.TENCENT_COS_BUCKET}.cos.{settings.TENCENT_COS_REGION}.myqcloud.com"

    def upload_video(
        self,
        local_file_path: str,
        remote_filename: str,
        subdir: Optional[str] = None
    ) -> Optional[str]:
        """
        上传视频到CDN

        Args:
            local_file_path: 本地文件路径
            remote_filename: 远程文件名
            subdir: 子目录（可选）

        Returns:
            公共访问URL或None
        """
        if not self.client:
            print("CDN client not initialized")
            return None

        # 构建远程路径
        if self.provider == "aliyun":
            object_key = self._build_object_key(settings.OSS_VIDEO_PATH, subdir, remote_filename)
            return self._upload_aliyun(local_file_path, object_key)
        elif self.provider == "tencent":
            object_key = self._build_object_key("videos/exercises/", subdir, remote_filename)
            return self._upload_tencent(local_file_path, object_key)

        return None

    def upload_image(
        self,
        local_file_path: str,
        remote_filename: str,
        subdir: Optional[str] = None
    ) -> Optional[str]:
        """
        上传图片到CDN

        Args:
            local_file_path: 本地文件路径
            remote_filename: 远程文件名
            subdir: 子目录（可选）

        Returns:
            公共访问URL或None
        """
        if not self.client:
            print("CDN client not initialized")
            return None

        # 构建远程路径
        if self.provider == "aliyun":
            object_key = self._build_object_key(settings.OSS_IMAGE_PATH, subdir, remote_filename)
            return self._upload_aliyun(local_file_path, object_key)
        elif self.provider == "tencent":
            object_key = self._build_object_key("images/", subdir, remote_filename)
            return self._upload_tencent(local_file_path, object_key)

        return None

    def _build_object_key(self, base_path: str, subdir: Optional[str], filename: str) -> str:
        """构建对象键"""
        key = base_path
        if subdir:
            key = f"{key}{subdir}/"
        key = f"{key}{filename}"
        return key

    def _upload_aliyun(self, local_file_path: str, object_key: str) -> Optional[str]:
        """使用阿里云OSS上传"""
        try:
            self.client.put_object_from_file(object_key, local_file_path)
            return f"{self.base_url}/{object_key}"
        except Exception as e:
            print(f"Aliyun OSS upload failed: {e}")
            return None

    def _upload_tencent(self, local_file_path: str, object_key: str) -> Optional[str]:
        """使用腾讯云COS上传"""
        try:
            with open(local_file_path, 'rb') as f:
                self.client.put_object(
                    Bucket=settings.TENCENT_COS_BUCKET,
                    Body=f,
                    Key=object_key
                )
            return f"{self.base_url}/{object_key}"
        except Exception as e:
            print(f"Tencent COS upload failed: {e}")
            return None

    def generate_presigned_url(
        self,
        object_key: str,
        expires: int = 3600
    ) -> Optional[str]:
        """
        生成临时访问URL

        Args:
            object_key: 对象键
            expires: 过期时间（秒）

        Returns:
            临时URL或None
        """
        if not self.client:
            return None

        if self.provider == "aliyun":
            try:
                return self.client.sign_url('GET', object_key, expires)
            except Exception as e:
                print(f"Failed to generate presigned URL: {e}")
        elif self.provider == "tencent":
            try:
                return self.client.get_presigned_url(
                    Method='GET',
                    Bucket=settings.TENCENT_COS_BUCKET,
                    Key=object_key,
                    Expires=expires
                )
            except Exception as e:
                print(f"Failed to generate presigned URL: {e}")

        return None

    def delete_object(self, object_key: str) -> bool:
        """
        删除CDN上的对象

        Args:
            object_key: 对象键

        Returns:
            是否成功
        """
        if not self.client:
            return False

        try:
            if self.provider == "aliyun":
                self.client.delete_object(object_key)
            elif self.provider == "tencent":
                self.client.delete_object(
                    Bucket=settings.TENCENT_COS_BUCKET,
                    Key=object_key
                )
            return True
        except Exception as e:
            print(f"Failed to delete object: {e}")
            return False

    def list_objects(
        self,
        prefix: str,
        max_keys: int = 100
    ) -> list:
        """
        列出CDN上的对象

        Args:
            prefix: 前缀
            max_keys: 最大数量

        Returns:
            对象列表
        """
        if not self.client:
            return []

        try:
            if self.provider == "aliyun":
                result = oss2.ObjectIterator(self.client, prefix=prefix, max_keys=max_keys)
                return [{"key": obj.key, "size": obj.size, "last_modified": obj.last_modified} for obj in result]
            elif self.provider == "tencent":
                response = self.client.list_objects(
                    Bucket=settings.TENCENT_COS_BUCKET,
                    Prefix=prefix,
                    MaxKeys=max_keys
                )
                return [{"key": obj["Key"], "size": obj["Size"], "last_modified": obj["LastModified"]}
                       for obj in response.get("Contents", [])]
        except Exception as e:
            print(f"Failed to list objects: {e}")

        return []

    def get_file_info(self, object_key: str) -> Optional[dict]:
        """
        获取文件信息

        Args:
            object_key: 对象键

        Returns:
            文件信息或None
        """
        if not self.client:
            return None

        try:
            if self.provider == "aliyun":
                info = self.client.get_object_meta(object_key)
                return {
                    "size": int(info.get("Content-Length", 0)),
                    "content_type": info.get("Content-Type", ""),
                    "last_modified": info.get("Last-Modified", "")
                }
            elif self.provider == "tencent":
                response = self.client.head_object(
                    Bucket=settings.TENCENT_COS_BUCKET,
                    Key=object_key
                )
                return {
                    "size": response.get("Content-Length", 0),
                    "content_type": response.get("Content-Type", ""),
                    "last_modified": response.get("Last-Modified", "")
                }
        except Exception as e:
            print(f"Failed to get file info: {e}")

        return None

    def is_available(self) -> bool:
        """检查CDN服务是否可用"""
        return self.client is not None

    def get_base_url(self) -> str:
        """获取CDN基础URL"""
        return getattr(self, "base_url", "")


def get_cdn_service(provider: str = "aliyun") -> CDNService:
    """
    获取CDN服务实例

    Args:
        provider: CDN提供商 ("aliyun" 或 "tencent")

    Returns:
        CDNService实例
    """
    return CDNService(provider=provider)


# 便捷函数
def upload_exercise_video(
    local_file_path: str,
    filename: str,
    exercise_type: Optional[str] = None,
    provider: str = "aliyun"
) -> Optional[str]:
    """
    上传运动视频

    Args:
        local_file_path: 本地文件路径
        filename: 文件名
        exercise_type: 运动类型（作为子目录）
        provider: CDN提供商

    Returns:
        公共访问URL或None
    """
    cdn = get_cdn_service(provider)
    return cdn.upload_video(local_file_path, filename, subdir=exercise_type)


def upload_exercise_image(
    local_file_path: str,
    filename: str,
    image_type: str = "covers",
    provider: str = "aliyun"
) -> Optional[str]:
    """
    上传运动图片

    Args:
        local_file_path: 本地文件路径
        filename: 文件名
        image_type: 图片类型 (covers, steps)
        provider: CDN提供商

    Returns:
        公共访问URL或None
    """
    cdn = get_cdn_service(provider)
    return cdn.upload_image(local_file_path, filename, subdir=image_type)
