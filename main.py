from web import create_app, start2

app = create_app() 
if __name__ == '__main__':
    #print(start2())
    app.run()