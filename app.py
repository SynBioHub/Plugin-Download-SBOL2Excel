"""
This module features all of the endpoints for the Excel2SBOL converter.

One the functions are called, your results will be properly output.
"""

from flask import Flask
from flask import request
from flask import abort
from flask import send_from_directory
import os
import tempfile
import sbol2excel.converter as conv
import sys
import traceback
import requests

app = Flask(__name__)


@app.route("/status")
def status():
    """Status endpoint returns the status of the plug-in."""
    return("The SBOL2Excel Download Plug-In is currently running.")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    """Evalute endpoint returns a statement the validity of rdf type."""
    data = request.get_json(force=True)
    rdf_type = data['type']

    # REPLACE THIS SECTION WITH OWN RUN CODE
    # uses rdf types
    accepted_types = {'Collection'}

    acceptable = rdf_type in accepted_types

    # #to ensure it shows up on all pages
    # acceptable = True
    # END SECTION

    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415


@app.route("/run", methods=["POST"])
def run():
    """Run endpoint handles the running of the plug-in."""
    # delete if not needed
    # cwd = os.getcwd()

    # temporary directory to write intermediate files to
    temp_dir = tempfile.TemporaryDirectory()
    del_temp_dir = tempfile.TemporaryDirectory()

    data = request.get_json(force=True)

    complete_sbol = data['complete_sbol']
    imported_xml = requests.get(complete_sbol)

    # print(complete_sbol)

    try:
        # REPLACE THIS SECTION WITH OWN RUN CODE
        # pull the complete_sbol
        new_xml = 'temporary.xml'
        temp_xml = os.path.join(del_temp_dir.name, new_xml)
        with open(temp_xml, "w") as f:
            f.write(imported_xml.text)

        out_name = "Out.xlsx"
        download_file_name = os.path.join(temp_dir.name, out_name)
        conv.converter(temp_xml, download_file_name)
        # END SECTION

        return send_from_directory(
            temp_dir.name, out_name,
            as_attachment=True, attachment_filename=out_name)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        lnum = exc_tb.tb_lineno
        abort(
            415,
            f'Exception is: {e}, exc_type: {exc_type}, exc_obj: {exc_obj}, fname: {fname}, line_number: {lnum}, traceback: {traceback.format_exc()}')
