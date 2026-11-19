from django.db import migrations


COURSES = (
    "Informática para Internet",
    "Edificações",
    "Meio Ambiente",
    "Licenciatura em Matemática",
)


def create_courses(apps, schema_editor):
    PerfilFormacao = apps.get_model("linkif", "PerfilFormacao")
    for name in COURSES:
        PerfilFormacao.objects.using(schema_editor.connection.alias).get_or_create(nome=name)


def delete_courses(apps, schema_editor):
    PerfilFormacao = apps.get_model("linkif", "PerfilFormacao")
    PerfilFormacao.objects.using(schema_editor.connection.alias).filter(nome__in=COURSES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("linkif", "0008_noticia"),
    ]

    operations = [
        migrations.RunPython(create_courses, delete_courses),
    ]