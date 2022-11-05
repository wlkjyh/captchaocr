import ddddocr, base64, cv2, requests, time,json,threading,configparser,os
from flask import Flask, request

# 读取service.conf配置文件
config = configparser.ConfigParser()
config.read('service.conf',encoding='utf-8')
service = config['service']

app = Flask(__name__)

ddddocr_list = []
ddddocr_state = []

def init():
    t = service['worker_threads']
    t = int(t)
    for i in range(t):
        ddddocr_list.append(ddddocr.DdddOcr())
        ddddocr_state.append(0)
        os.system('cls')

    print("init success")

def get_ddddocr():
    for i in range(len(ddddocr_state)):
        if ddddocr_state[i] == 0:
            ddddocr_state[i] = 1
            return i
    return -1

def destroy_ddddocr(i):
    ddddocr_state[i] = 0
    return 0

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        file = request.files['file']
        if file is None:
            return json.dumps({'code': False, 'msg': '服务器错误'})
        filename = file.filename
        # 判断是不是图片
        if filename.split('.')[-1] not in ['jpg', 'png', 'jpeg']:
            return json.dumps({'code': False, 'msg': '这不是有效的图片'})

        content = file.read()
        i = get_ddddocr()
        if i == -1:
            return json.dumps({'status': False, 'msg': '没有空闲的OCR线程'})
        print("已调度线程", i)
        starttime = time.time()
        data = ddddocr_list[i].classification(content)
        endtime = time.time()
        destroy_ddddocr(i)
        print("线程", i, "已释放")
        return json.dumps({'status': True, 'msg': 'SUCCESS', 'result': data,'usage': endtime - starttime})
    except Exception as e:
        return json.dumps({'status': False, 'msg': str(e)})
if __name__ == '__main__':
    threading.Thread(target=init).start()
    app.run(host=service['listen'], port=service['port'], debug=False)
