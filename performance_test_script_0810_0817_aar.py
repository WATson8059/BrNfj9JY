# 代码生成时间: 2025-08-10 08:17:36
import requests
import time
from locust import HttpUser, task, between

class PyramidUser(HttpUser):
    # 定义性能测试的基本URL
    host = "http://localhost:6543"  # 假设Pyramid应用运行在本地的6543端口

    # 发送GET请求
    @task
    def get_index(self):
        try:
            response = self.client.get("/")
            # 确保响应状态码为200，如果不是，则记录错误
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error accessing index page: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error during requests to index page: {e}")

    # 发送POST请求
    @task
    def post_data(self):
        try:
            response = self.client.post("/data", json={"key": "value"}, catch_response=True)
            # 确保响应状态码为200，如果不是，则记录错误
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error accessing data: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error during requests to data: {e}")

    # 定义任务间的等待时间（在0.5秒到1秒之间变化）
    wait_time = between(0.5, 1)

# 运行性能测试脚本的入口点
if __name__ == '__main__':
    # 运行Locust性能测试
    from locust import run_single_process
    run_single_process(PyramidUser)