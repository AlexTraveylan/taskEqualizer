# Une api pour partager les taches menageres

## Description

Cette api permet de partager des taches menageres entre les membres d'une famille.

## Technologies

python 3.12
django
django-ninja
...

## Deploy command

```bash
gunicorn --bind 0.0.0.0:8000 TaskEqualizer.wsgi:application
```