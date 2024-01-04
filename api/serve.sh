#!/bin/bash
exec poetry run gunicorn -b :5000 app:app