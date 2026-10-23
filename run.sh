#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
streamlit run streamlit_app.py
