import webview
import os

def load_html():
    cwd = os.getcwd()
    html_file = f'file://{cwd}/templates/index.html'
    return html_file

if __name__ == '__main__':
    window = webview.create_window('Yolo Expert', load_html(), width=1280, height=720)
    webview.start()
