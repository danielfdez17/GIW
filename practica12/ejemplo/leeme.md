Para ejecutar este ejemplo debéis:

1) Crear las migraciones
   
        $ python manage.py makemigrations opiniones
    
2) Aplicar las migraciones
       
       $ python manage.py migrate
   
3) Crear un superusuario
     
       $ python manage.py createsuperuser
   
4) Lanzar el servidor
   $ python manage.py runserver

5) Acceder a la interfaz grafica de administración http://127.0.0.1:8000/admin/
   como superusuario y añadir usuarios normales

6) Acceder a la aplicación web 127.0.0.1:8000/opiniones/ con usuarios normales y
   añadir opiniones
