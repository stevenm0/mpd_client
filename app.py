from flask import Flask, request, jsonify
import mpd

app = Flask(__name__)
mpd_client = mpd.MPDClient(use_unicode=True)

@app.route("/music", methods=["GET"])
def get_all_music():
  mpd_client.connect("localhost", 6600)
  list_info = mpd_client.lsinfo("/")
  mpd_client.disconnect()
  return jsonify(list_info)

@app.route("/music/<artist>", methods=["GET"])
def get_music_artist(artist):
  mpd_client.connect("localhost", 6600)
  list_info = mpd_client.lsinfo(artist)
  mpd_client.disconnect()
  return jsonify(list_info)

@app.route("/files", methods=["GET"])
def get_all_songs():
  mpd_client.connect("localhost", 6600)
  list_info = mpd_client.listall("/")
  mpd_client.disconnect()
  return jsonify(list_info)

@app.route("/files/<directory>", methods=["GET"])
def get_songs_dir(directory):
  mpd_client.connect("localhost", 6600)
  list_info = mpd_client.listall(directory)
  mpd_client.disconnect()
  return jsonify(list_info)

@app.route("/files/<directory>/<filename>", methods=["GET"])
def get_songs_file(directory, filename):
  mpd_client.connect("localhost", 6600)
  list_info = mpd_client.listall(directory + "/" + filename)
  mpd_client.disconnect()
  return jsonify(list_info)

@app.route("/status", methods=["GET"])
def get_status():
  mpd_client.connect("localhost", 6600)
  status = mpd_client.status()
  mpd_client.disconnect()
  return jsonify(status)

@app.route("/status/<status_id>", methods=["GET"])
def get_status_id(status_id):
  mpd_client.connect("localhost", 6600)
  if status_id in mpd_client.status():
    status = mpd_client.status()[status_id]
  else:
    status = {"ERROR": "Status Key Not Found"}
  mpd_client.disconnect()
  return jsonify({status_id: status})

@app.route("/play", methods=["GET"])
def press_play():
  mpd_client.connect("localhost", 6600)
  mpd_client.play()
  state = mpd_client.status()['state']
  mpd_client.disconnect()
  return jsonify({"state": state})

@app.route("/pause", methods=["GET"])
def press_pause():
  mpd_client.connect("localhost", 6600)
  mpd_client.pause()
  state = mpd_client.status()['state']
  mpd_client.disconnect()
  return jsonify({"state": state})

@app.route("/state", methods=["PUT"])
def change_state():
  # Ensure we were given valid json
  if (request.headers['Content-Type'] == 'application/json'
      and 'state' in request.json):
    mpd_client.connect("localhost", 6600)
    # If state requested is 'play'
    if (request.json['state'] == 'play'
        and mpd_client.status()['state'] != 'play'):
      mpd_client.play()
    # Otherwise if state requested is 'pause'
    elif (request.json['state'] == 'pause'
          and mpd_client.status()['state'] != 'pause'):
      mpd_client.pause()
    # Retrieve what the state is now and return
    # that to the requester
    state = mpd_client.status()['state']
    mpd_client.disconnect()
    return jsonify({"state": state})
  else:
    return jsonify({"error": "invalid json submitted"})


if __name__ == '__main__':
    app.run(debug=True)
