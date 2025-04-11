from flask import Blueprint, render_template, redirect

files_process = Blueprint("files_process",__name__)

@files_process.route("/")
def mainPage ():
    return render_template("files_process/grabar_audio.html")

@files_process.route("/upload", methods=["POST"])
def dataUpload ():
    print("LLEGO")
    return ""