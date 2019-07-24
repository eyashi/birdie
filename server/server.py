import os
import datetime
from flask import Flask, jsonify

# init log
log_file_name = "bird_present_log.txt"
if not os.path.isfile(log_file_name):
    open(log_file_name, "a").close()

# init the flask app
app = Flask(__name__)

# default page reports status of all elements.
# or something like that.
@app.route("/")
def report_status():
    return "Hello World!"


@app.route("/evaluate")
def evaluate_new_clip():
    pass


@app.route("/increment-count")
def increment_bird_counter():
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open(log_file_name, "a") as l:
        l.write("BIRD! @{}\n".format(time_stamp))

    resp = jsonify(success=True)
    return resp


@app.route("/update-dashboard")
def update_dashboard():
    # when called will update the dashboard display of birds.
    pass


if __name__ == "__main__":
    app.run()
