# Grand Realty - Real Estate Platform

Platforme Real Estate e ndertuar me Django, PostgreSQL dhe Django built-in authentication.

## Funksionalitetet

- Shfaqje publike e pronave dhe detajeve te tyre
- Kerkim sipas titullit dhe vendndodhjes
- Filtrim sipas cmimit minimal/maksimal, dhomave dhe llojit te prones
- Login dhe register ne nje faqe te vetme
- Dashboard "Llogaria jote"
- Shtim pronash nga cdo user i loguar
- Favorite per prona te ruajtura
- Mesazhe mes userave per prona specifike
- Galeri fotosh ne faqen e detajit
- UI ne shqip

## Teknologjite

- Python 3.13+
- Django 6
- PostgreSQL
- Pillow per upload/menaxhim imazhesh
- HTML, CSS, JavaScript

## Instalimi

Krijo dhe aktivizo virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instalo paketat:

```powershell
pip install -r requirements.txt
```

## Databaza

Projekti eshte konfiguruar per PostgreSQL ne `config/settings.py`.

Krijo nje databaze me emrin:

```text
real_estate
```

Pastaj apliko migrimet:

```powershell
python manage.py migrate
```

Krijo superuser per admin panel:

```powershell
python manage.py createsuperuser
```

## Nisja e projektit

```powershell
python manage.py runserver
```

Hap faqen:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## URL kryesore

- `/` - Kryefaqja
- `/listings/` - Lista e pronave
- `/property/<id>/` - Detajet e prones
- `/login/` - Auth page me Login/Register
- `/register/` - E njejta Auth page, hap tab-in Register
- `/account/` - Dashboard i userit
- `/properties/new/` - Shto prone

## Komanda te dobishme

Kontrollo projektin:

```powershell
python manage.py check
```

Krijo migrime pas ndryshimeve ne modele:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Ekzekuto testet:

```powershell
python manage.py test
```

## Struktura kryesore

```text 
base/
  models.py       Modelet: Property, Favorite, Message, Agent
  views.py        Logjika e faqeve
  forms.py        Format per auth, prona, mesazhe, kontakt
  urls.py         URL-te e app-it
  templates/      HTML templates
  static/         CSS, JavaScript, imazhe

config/
  settings.py     Konfigurimi i Django
  urls.py         URL kryesore te projektit
```

## Shenime

Per te shtuar prona, ruajtur favorite ose derguar mesazhe, useri duhet te jete i loguar. Vizitoret pa login mund te shohin listen e pronave dhe detajet e tyre.
