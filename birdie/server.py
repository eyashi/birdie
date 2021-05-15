import os
import datetime
from flask import Flask, jsonify

from database import Database

# init log for debugging
log_file_name = "bird_present_log.txt"
if not os.path.isfile(log_file_name):
    open(log_file_name, "a").close()

unprocessed_clip_dir = os.path.join("recordings", "unprocessed")

# initialize prediction engine
predictor = Predictor()

# initialize the database
db = Database()

# initialize the flask app
app = Flask(__name__)

# default page reports status of all elements.
# or something like that.
@app.route("/")
def report_status():
    birds, no_birds = db.return_counts()
    return "Clips with birds present: {0}\nClips with no birds present: {1}".format(
        birds, no_birds
    )


@app.route("/evaluate")
def evaluate_new_clip():
    dir_contents = os.listdir(unprocessed_clip_dir)
    if len(dir_contents) > 0:
        try:
            for new_clip in dir_contents:
                clip_name, pred = predictor.predict(new_clip)

                # update the database, leaving the two other predictions aside for later.
                db.update([clip_name, pred, None, None])

            return jsonify(status="clips processed", success=True)
        except Exception as e:
            return jsonify(status="error", success=False)

    else:
        resp = jsonify(status="no clips", success=True)
        return resp


if __name__ == "__main__":
    app.run()
