python manage.py migrate --check
status=$$?
if [[ $$status -eq 0 ]]
  then echo -e '\033[0;33m'"Migrations are not detected."
else
  echo  -e '\033[0;31m'"Unapplied migrations are detected!"
  python manage.py makemigrations
  python manage.py migrate
  python manage.py loadall
fi
python manage.py runserver 0.0.0.0:8000 --noreload