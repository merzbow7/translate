from json import loads

from flask import render_template, redirect, url_for, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app import app, db
from english_tool import get_words_from_url
from forms import URLForm
from models import Translate, Song


@app.route("/", methods=["GET", "POST"])
def index():
    url_form = URLForm()
    if url_form.validate_on_submit():
        return redirect(url_for('exercise', from_url=url_form.url.data))
    return render_template("index.html",
                           url_form=url_form,
                           )


@app.route("/words/<count>", methods=["GET"])
def words_count(count):
    if isinstance(count, int) or count.isdigit():
        return jsonify({item.en: item.ru for item in Translate.query.all()[:int(count)]})
    else:
        return jsonify({"error": "bad count",
                        "url": f"{request.url}",
                        "correct_url": f"{request.url_root}words/<count>",
                        })


@app.route("/songs/<name>/lyric", methods=["GET"])
def lyric(name):
    song = Song.query.filter_by(title=name)
    if song:
        text = song.first().lyrics
        return jsonify({"title": name,
                        "lyric": text})
    else:
        return jsonify({"error": "bad name",
                        "url": f"{request.url}",
                        })


@app.route("/words", methods=["GET"])
def get_words():
    return render_template("words.html")


@app.route("/words/json", methods=["GET", "POST"])
def get_translate():
    if request.method == "POST":
        data = loads(request.get_data())
        words = data.get("words", False)
        print(data)
        error = False
        error_name = ""
        if words:
            for word_en, word_ru in words.items():
                translate = Translate(en=word_en, ru=word_ru)
                try:
                    db.session.add(translate)
                    db.session.commit()
                except Exception as err:
                    error = True
                    error_name = err
                    db.session.rollback()
        if error:
            return {"status": "error", "name": error_name}
        else:
            return {"status": "ok"}
    if request.method == "GET":
        words = request.args
        result = {"words": {}}
        if words:
            for item in words:
                translate = Translate.query.filter_by(en=item).first()
                if translate:
                    result["words"][item] = translate.ru
                else:
                    result["words"][item] = None
            return jsonify(result)


@app.route("/exercise")
def exercise():
    request_page = request.args.get('from_url')
    if request_page:
        content = get_words_from_url(request_page)
    else:
        content = Translate.query.all()
    return render_template("exercise.html",
                           main_content=content[:8],
                           )


@app.route("/songs")
def songs():
    songs = [song.title for song in Song.query.all()]
    return render_template("songs.html", songs=songs)


@app.route("/songs/<name>")
def songs_name(name):
    return render_template("song_test.html")
