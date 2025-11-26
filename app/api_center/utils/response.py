from typing import Any, Dict, Optional, Union, Tuple


def api_response(data: Any = None, code: int = 0, msg: str = "") -> Dict[str, Any]:
    """
    统一的API响应格式
    
    Args:
        data: 返回的数据
        code: 状态码，0表示成功，大于0表示错误
        msg: 消息，通常在错误时使用
        
    Returns:
        统一格式的响应字典: {code: int, msg: str, data: Any}
    """
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

def success(data: Any = None, msg: str = "") -> Dict[str, Any]:
    """
    成功响应
    
    Args:
        data: 返回的数据
        msg: 成功消息
        
    Returns:
        成功的响应字典
    """
    return api_response(data=data, code=0, msg=msg)

def error(msg: str, code: int = 1, data: Any = None) -> Dict[str, Any]:
    """
    错误响应
    
    Args:
        msg: 错误消息
        code: 错误码，默认为1（通用错误）
        data: 额外的错误数据
        
    Returns:
        错误的响应字典
    """
    return api_response(data=data, code=code, msg=msg)

def handle_response(result: Union[Dict[str, Any], Tuple[Dict[str, Any], int]]) -> Tuple[Dict[str, Any], int]:
    """
    处理各种响应格式，转换为统一格式
    
    Args:
        result: 原始响应结果，可能是字典或(字典, 状态码)元组
        
    Returns:
        统一格式的响应元组: (响应字典, HTTP状态码)
    """
    if isinstance(result, tuple) and len(result) == 2:
        data, status_code = result
        # 如果已经是统一格式，直接返回
        if isinstance(data, dict) and all(k in data for k in ["code", "msg", "data"]):
            return data, status_code
        # 否则转换为统一格式
        return success(data=data), status_code
    else:
        # 如果只有数据没有状态码，默认200
        if isinstance(result, dict) and all(k in result for k in ["code", "msg", "data"]):
            return result, 200
        return success(data=result), 200
