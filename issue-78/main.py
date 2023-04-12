import requests
import time
import os
from proxies import proxy_list


def test_proxy(file_url, test_proxy):

    t0 = time.time()
    response = requests.get(
        file_url,
        stream=True,
        proxies={
            test_proxy.split(":")[0]: test_proxy
        },  # The split here fetches the protocol of the proxy so we can pass both https and http proxies
    )
    open(f"file", "wb").write(response.content)
    size = response.headers.get("content-length", 0)

    while not os.path.isfile("file"):
        time.sleep(0.1)
    t1 = time.time()

    os.remove("file")  # Deletes the file after testing the proxy

    return int(size) / 1000000 / (t1 - t0)


proxies = proxy_list


url = "http://download.kiwix.org/other/translate_www.kiwix.org_tutorial.mp4"  # Enter the file that needs to be donwloaded for each proxy
result = {}

for proxy in proxies:

    # This 'if' is to ensure we dont check the same country's proxy again
    if proxy[0] not in result.keys():
        try:
            speed = test_proxy(url, proxy[1])
            result[proxy[0]] = [proxy[1], speed]

        except:
            print(
                f"{proxy[0]} proxy **({proxy[1]})** didnt work, moving to the next one.."
            )
            continue

# This writes the result dictionary to result text file
with open("results.txt", "w") as file:

    for key in result.keys():
        file.write(f"{key},{result[key][0]},{result[key][1]}\n")

os.system("python api.py")
