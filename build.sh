# Install dependencies
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Collect static files for Django
python3 manage.py collectstatic --noinput

# Run Django migrations
python3 manage.py migrate

# Start Django server (Vercel will use this as entrypoint)
python3 manage.py runserver 0.0.0.0:$PORT
