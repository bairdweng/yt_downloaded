# -*- coding: UTF-8 -*-


from sanic.response import json, text
from sanic import Sanic, request
import subprocess


app = Sanic("yt")
app.config.HEALTH = True


@app.route("/yt/url", methods=["POST"])
async def calculate_add(request):
    """ 分类 """
    if request.method == "POST":
        params = request.form if request.form else request.json
    else:
        params = {}
    url = params.get("url", 0)
    data_dict = {"url": url}
    try:
        result = subprocess.call(["yt-dlp -g " + url], shell=True)
        # data_dict = {"url": result}
        # print(result.stdout)
        result = subprocess.run(["yt-dlp -g " + url],
                                stdout=subprocess.PIPE, text=True, shell=True)
        data_dict = {"url": result.stdout}
        # print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("命令执行失败，返回码:", e.returncode)
        print("错误输出:", e.stderr)

    status_code = 200
    res_dict = {"code": status_code,
                "data": data_dict,
                "message": "success"
                }
    return json(res_dict, status=status_code, ensure_ascii=False)


if __name__ == "__main__":
    app.run(single_process=True,
            access_log=True,
            host="0.0.0.0",
            port=8032,
            workers=1,
            )
