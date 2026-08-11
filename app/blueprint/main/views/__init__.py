from flask import render_template, abort, redirect, url_for, jsonify, flash, request


def index():
    return 'Hello, World from the Blueprint.'