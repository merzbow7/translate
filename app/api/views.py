from json import loads

from flask import render_template, request, jsonify, Response

from app import db
from app.api import bp
from app.models import Translate, Song
from utils.parse_words import make_en_ru_dict


@bp.route("/api/words/<count>", methods=["GET"])
def words_count(count):
    if isinstance(count, int) or count.isdigit():
        return jsonify({item.en: item.ru for item in Translate.query.all()[:int(count)]})
    else:
        return jsonify({"error": "bad count",
                        "url": f"{request.url}",
                        "correct_url": f"{request.url_root}words/<count>",
                        })


@bp.route("/api/songs/<name>/lyric", methods=["GET"])
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


@bp.route("/api/words/json", methods=["GET", "POST"])
def get_translate():
    if request.method == "POST":
        data = loads(request.get_data())
        words = data.get("words", False)
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


@bp.route("/api/exercise")
def exercise():
    request_page = request.args.get('from_url')
    if request_page:
        content = make_en_ru_dict(request_page)
        template = "url_exercise.html"
    else:
        content = Translate.query.all()
        template = "exercise.html"
    return render_template(template, main_content=content[:20], )


@bp.route("/api/songs")
def songs():
    return jsonify([song.title for song in Song.query.all()])


@bp.route("/api/songs/<name>")
def songs_name(name):
    return jsonify(Song.query.filter_by(songs_name=name).first())
