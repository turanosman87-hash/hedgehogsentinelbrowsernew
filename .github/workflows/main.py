import sys
from PyQt6.QtCore import QUrl # Burayı PyQt5 yapıyoruz aşağıda
try:
    from PyQt5.QtCore import QUrl
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
except ImportError:
    print("Sistemde PyQt5 eksik!")

BLOCKED = ["facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com"]
CLEAN_JS = "function h(){['#comments','ytd-comments','#chat'].forEach(s=>{document.querySelectorAll(s).forEach(el=>el.remove())})}setInterval(h,2000);"

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if any(site in url.toString().lower() for site in BLOCKED): return False
        return True

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel (Classic Edition)")
        self.resize(1100, 750)
        c = QWidget(); self.setCentralWidget(c)
        l = QVBoxLayout(c); l.setContentsMargins(0,0,0,0)
        self.url_bar = QLineEdit(); self.url_bar.returnPressed.connect(self.navigate)
        l.addWidget(self.url_bar)
        self.browser = QWebEngineView()
        self.browser.setPage(SentinelPage(self.browser))
        self.browser.loadFinished.connect(lambda: self.browser.page().runJavaScript(CLEAN_JS))
        l.addWidget(self.browser)
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate(self):
        u = self.url_bar.text()
        self.browser.setUrl(QUrl(u if "://" in u else "https://" + u))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HedgehogBrowser()
    window.show()
    sys.exit(app.exec())

