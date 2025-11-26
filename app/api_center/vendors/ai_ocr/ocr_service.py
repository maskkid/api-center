"""
OCR 服务实现
提供基于 PaddleOCR 的文字识别功能
"""

from paddleocr import PaddleOCR
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import cv2
import requests
import io
import base64
import os

from api_center.utils.decorators import decorate_requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    """OCR 服务类，提供图像文字识别功能"""
    _instance = None
    _wx_ocr_url = "http://192.168.1.24:5000/ocr"  # 微信OCR服务地址
    
    @classmethod
    def get_instance(cls) -> PaddleOCR:
        """获取 PaddleOCR 实例（单例模式）"""
        if cls._instance is None:
            cls._instance = PaddleOCR(use_angle_cls=True, lang='ch')
        return cls._instance
    
    @staticmethod
    def process_image(image) -> Dict[str, Any]:
        """
        处理图片并返回OCR结果
        
        Args:
            image: 图像数据，可以是 OpenCV 格式的图像
            
        Returns:
            Dict[str, Any]: 包含识别结果列表和合并后文本的字典
        """
        ocr = OCRService.get_instance()
        try:
            result = ocr.ocr(image, cls=True)
            if not result or not result[0]:
                return {
                    'results': [],
                    'results_text': ''
                }
                
            processed_result = []
            # 按照 y 坐标排序，将同一行的文本合并
            sorted_lines = sorted(result[0], key=lambda x: (
                sum(p[1] for p in x[0])/4  # 计算 y 坐标的平均值
            ))
            
            # 初始化变量
            current_y = None
            line_threshold = 10  # 同一行的 y 坐标差异阈值
            current_line = []
            lines = []
            
            # 按行分组
            for line in sorted_lines:
                y = sum(p[1] for p in line[0])/4  # 当前文本块的平均 y 坐标
                
                if current_y is None:
                    current_y = y
                    current_line.append(line)
                elif abs(y - current_y) <= line_threshold:
                    current_line.append(line)
                else:
                    lines.append(current_line)
                    current_line = [line]
                    current_y = y
            
            if current_line:
                lines.append(current_line)
            
            # 处理每一行，按 x 坐标排序
            for idx, line in enumerate(sorted_lines):
                processed_result.append({
                    'index': idx + 1,
                    'text': line[1][0],
                    'confidence': float(line[1][1]),
                    'position': line[0]
                })
            
            # 合并所有文本，保持原有顺序和换行
            merged_text = ""
            for line in lines:
                # 按 x 坐标排序每一行的文本
                sorted_line = sorted(line, key=lambda x: min(p[0] for p in x[0]))
                line_text = " ".join(text[1][0] for text in sorted_line)
                if merged_text:
                    merged_text += "\n"
                merged_text += line_text
            
            return {
                'results': processed_result,
                'results_text': merged_text
            }
        except Exception as e:
            logger.error(f"OCR处理错误: {str(e)}")
            raise
    
    @staticmethod
    def recognize_from_url(url: str, language: str = 'ch') -> Dict[str, Any]:
        """
        从 URL 获取图像并进行文字识别
        
        Args:
            url: 图像的 URL
            language: 识别语言，默认为中文 'ch'
            
        Returns:
            Dict: 包含语言和识别结果的字典
            
        Raises:
            requests.exceptions.RequestException: 下载图像时出错
            Exception: 处理图像时出错
        """
        # 下载图片
        response = decorate_requests(requests).get(url, timeout=10)
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Failed to download image: {response.status_code}")
            
        # 将图片内容转换为OpenCV格式
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # 处理OCR
        result = OCRService.process_image(image)
        result['language'] = language
        
        return result
    
    @staticmethod
    def recognize_from_file(file_data, language: str = 'ch') -> Dict[str, Any]:
        """
        从文件数据进行文字识别
        
        Args:
            file_data: 文件数据，可以是 FileStorage 对象或二进制数据
            language: 识别语言，默认为中文 'ch'
            
        Returns:
            Dict: 包含语言和识别结果的字典
            
        Raises:
            Exception: 处理图像时出错
        """
        # 读取文件数据
        if hasattr(file_data, 'save'):  # FileStorage 对象
            in_memory_file = io.BytesIO()
            file_data.save(in_memory_file)
            image_array = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        else:  # 二进制数据
            image_array = np.frombuffer(file_data, dtype=np.uint8)
            
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # 处理OCR
        result = OCRService.process_image(image)
        result['language'] = language
        
        return result

    @classmethod
    def recognize_with_wx(cls, image_data: bytes, api_url: str = None) -> Dict[str, Any]:
        """
        使用微信OCR服务进行文字识别
        
        Args:
            image_data: 图像二进制数据
            api_url: 可选的API地址，如果不提供则使用默认地址
            
        Returns:
            Dict[str, Any]: 包含识别结果的字典
            
        Raises:
            Exception: 处理图像或API请求时出错
        """
        try:
            # 使用提供的API地址或默认地址
            api_url = api_url or cls._wx_ocr_url
            
            # 将图像数据转换为base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # 发送请求到API
            response = requests.post(api_url, json={"image": base64_image})
            response.raise_for_status()
            
            result = response.json()
            
            # 检查响应状态
            if result.get('result', {}).get('errcode') != 0:
                raise Exception(f"OCR API returned error: {result}")
            
            # 处理OCR结果
            ocr_response = result['result'].get('ocr_response', [])
            processed_result = []
            
            for idx, item in enumerate(ocr_response, 1):
                processed_result.append({
                    'index': idx,
                    'text': item['text'],
                    'confidence': float(item['rate']),
                    'position': [
                        [item['left'], item['top']],
                        [item['right'], item['top']],
                        [item['right'], item['bottom']],
                        [item['left'], item['bottom']]
                    ]
                })
            
            # 合并所有文本
            merged_text = "\n".join(item['text'] for item in ocr_response)
            
            return {
                'results': processed_result,
                'results_text': merged_text,
                'language': 'ch',  # 微信OCR默认中文
                'width': result['result'].get('width'),
                'height': result['result'].get('height')
            }
            
        except Exception as e:
            logger.error(f"微信OCR处理错误: {str(e)}")
            raise

    @classmethod
    def recognize_with_wx_from_url(cls, url: str, api_url: str = None) -> Dict[str, Any]:
        """
        从URL获取图像并使用微信OCR服务进行识别
        
        Args:
            url: 图像的URL
            api_url: 可选的API地址，如果不提供则使用默认地址
            
        Returns:
            Dict[str, Any]: 包含识别结果的字典
            
        Raises:
            requests.exceptions.RequestException: 下载图像时出错
            Exception: 处理图像时出错
        """
        try:
            # 下载图片
            response = decorate_requests(requests).get(url, timeout=10)
            response.raise_for_status()
            
            # 使用微信OCR服务处理
            return cls.recognize_with_wx(response.content, api_url)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"下载图像失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"微信OCR处理错误: {str(e)}")
            raise

    @classmethod
    def recognize_with_wx_from_file(cls, file_data, api_url: str = None) -> Dict[str, Any]:
        """
        从文件数据使用微信OCR服务进行识别
        
        Args:
            file_data: 文件数据，可以是FileStorage对象或二进制数据
            api_url: 可选的API地址，如果不提供则使用默认地址
            
        Returns:
            Dict[str, Any]: 包含识别结果的字典
            
        Raises:
            Exception: 处理图像时出错
        """
        try:
            # 读取文件数据
            if hasattr(file_data, 'save'):  # FileStorage对象
                in_memory_file = io.BytesIO()
                file_data.save(in_memory_file)
                image_data = in_memory_file.getvalue()
            else:  # 二进制数据
                image_data = file_data
                
            # 使用微信OCR服务处理
            return cls.recognize_with_wx(image_data, api_url)
            
        except Exception as e:
            logger.error(f"微信OCR处理错误: {str(e)}")
            raise
