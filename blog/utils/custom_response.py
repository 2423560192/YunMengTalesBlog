# backend/blog/utils.py
import logging

from rest_framework.response import Response
from rest_framework import status

# 配置日志


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置日志级别为 INFO
handler = logging.StreamHandler()  # 输出到控制台
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def custom_response(status="success", message="请求成功", data=None, status_code=status.HTTP_200_OK,
                    handle_exception=False):
    """
    自定义响应函数，返回统一格式的 JSON 响应，并支持日志记录和异常处理。

    Args:
        status (str): 状态，"success" 或 "error" (默认 "success")
        message (str): 消息描述 (默认 "请求成功")
        data (dict/list): 返回的数据 (默认 None)
        status_code (int): HTTP 状态码 (默认 200)
        handle_exception (bool): 是否启用内部异常处理 (默认 False)

    Returns:
        Response: 格式化的 JSON 响应

    Raises:
        Exception: 如果 handle_exception 为 False 且发生异常，则抛出
    """
    try:
        # 记录响应日志
        logger.info(f"Response: status={status}, message={message}, data={data}, status_code={status_code}")

        # 构造响应数据
        response_data = {
            "status": status,
            "message": message,
            "data": data
        }

        return Response(response_data, status=status_code)

    except Exception as e:
        logger.error(f"Error in custom_response: {str(e)}")
        if handle_exception:
            return custom_response(
                status="error",
                message=f"内部错误: {str(e)}",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        raise  # 如果 handle_exception 为 False，则抛出异常
