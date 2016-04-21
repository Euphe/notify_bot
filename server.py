import flask
import server_settings

bot = None
app = flask.Flask(__name__)
app.config["SERVER_NAME"] = server_settings.SERVER_NAME
@app.route("/<key>", methods=['POST'])
def send_notification(key):
    text = flask.request.form["text"]
    
    resp = bot.send_notification(key, text)
    if resp:
        return "Success"
    return ('Unknown key', 404)

def get_server_name():
    return app.config['SERVER_NAME']

def run_server(bot_):
    global bot
    bot = bot_
    app.run()

if __name__ == '__main__':
    app.run()