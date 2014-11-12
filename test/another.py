import urllib2
import json
import tarfile
import re
import os
from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.debug = True

registry_url = "localhost"
if "REGURL" in os.environ:
        registry_url = os.environ['REGURL']

print "Registry reside on http://" + str(registry_url)  + "/v1" 

FILE_TYPES = {
    'f':'file',
    'l':'hardlink',
    's':'symlink',
    'c':'char',
    'b':'block',
    'd':'directory',
    'i':'fifo',
    't':'cont',
    'L':'longname',
    'K':'longlink',
    'S':'sparse',
}

def _query(path):
    response = urllib2.urlopen("http://" + str(registry_url)  + "/v1" + str(path))
    result = json.loads(response.read())
    return result

def _build_file_dict(files):
    res = []
    for file in files:
        res.append({
            'name': file[0],
            'type': FILE_TYPES.get(file[1], 'unknown'),
            'deleted': file[2],
            'size': file[3],
            'mtime': file[4],
            'mode': file[5],
            'owner': file[6],
            'group': file[7]
         })
    return res

def _build_image_tree(images):
    all_images = []
    for image in images:
        d = _query("/images/%s/json" % image['id'])
        all_images.append(d)
    exists = set(map(lambda x : x['id'], all_images))
    top = [x for x in all_images if 'parent' not in x.keys()][0]
    children = {}
    for image in all_images:
        if 'parent' not in image.keys():
            continue
        parent = image['parent']
        if not parent:
            continue
        if parent not in exists:
            continue
        if parent in children:
            children[parent].append(image)
        else:
            children[parent] = [ image ]
    return _sort_image_list(children, top)

def _sort_image_list(children, top):
    res = [ top ]
    if top['id'] in children:
        for child in children[top['id']]:
            res += _sort_image_list(children, child)
    return res

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def index():
    query = ''
    images = []
    if request.method == 'POST':
        query = request.form['query']
    result = _query('/search?q=' + query)
    for repo in result['results']:
        repo_images = _query("/repositories/%s/images" % repo['name'])
        images.append({'container': repo['name'], 'images': repo_images})
    return render_template('index.html', results=result['results'], images=images)

@app.route("/images/<image_id>")
@app.route("/images/<image_id>/<repo_name>")
def images(image_id, repo_name=None):
    result = _query("/images/%s/json" % image_id)
    files_raw = _query("/images/%s/files" % image_id)
    files = _build_file_dict(files_raw)
    return render_template('image.html', results=result, files=files, repo=repo_name)

@app.route("/repo/<repo_name>/<image_id>")
def repo(repo_name, image_id):
    result = _query("/repositories/%s/%s/json" % (repo_name,image_id))
    images = _query("/repositories/%s/%s/images" % (repo_name,image_id))
    tags = _query("/repositories/%s/%s/tags" % (repo_name,image_id))
    properties = _query("/repositories/%s/%s/properties" % (repo_name,image_id))
    sorted_images = _build_image_tree(images)
    return render_template('repo.html', name=repo_name+"/"+image_id,
        results=result, images=sorted_images, tags=tags, properties=properties)

@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    value = re.sub(r'[0-9]{2}Z$','', value)
    d = datetime(*map(int, re.split('[^\d]', value)[:-1]))
    return d.strftime(format)

@app.template_filter()
def joinifarray(value):
    if type(value) == list:
        res = ' '.join(value)
    else:
        res = value
    return res

app.jinja_env.filters['datetimefilter'] = datetimefilter
app.jinja_env.filters['joinifarray'] = joinifarray

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)