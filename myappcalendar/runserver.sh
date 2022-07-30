python manage.py migrate --check
status=$?
if [[ $status -eq 0 ]]
  then echo -e "\e[1;102mMigrations are not detected!\e[0m"
else
  echo  -e "\e[1;41mUnapplied migrations are detected!\e[0m"
  python manage.py makemigrations
  python manage.py migrate
  python manage.py loadall
fi
python manage.py runserver 0.0.0.0:8000