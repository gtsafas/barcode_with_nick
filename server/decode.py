#!/usr/bin/env python

from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
import tornado.ioloop
import tornado.web
import json

INVENTORY = {
        "0123456789012": "Ketchup",
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")

class ItemsHandler(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        items = [
            {'name': 'Item 1'},
            {'name': 'Item 2'},
        ]
        self.write(json.dumps(items))

class UploadHandler(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)
        self.set_header('Access-Control-Allow-Origin', '*')

    def post(self):
        data = self.request.files['barcode_image'][0].body
        fileObj = BytesIO(data)
        image = Image.open(fileObj)
        barcode_id = process_barcode_image(image)

        self.write(json.dumps({'barcode_id': barcode_id, 'product': INVENTORY.get(barcode_id)}))



def start_server():
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/items", ItemsHandler),
        (r"/upload", UploadHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

def process_barcode_image(image):
    decoded = decode(image)
    if decoded:
        return decoded[0].data.decode('utf-8')

def main():
    image = Image.open('barcode3.jpeg')

    inventory_id = process_barcode_image(image)
    print(inventory_id)
    
    start_server()




if __name__ == '__main__':
    main()
