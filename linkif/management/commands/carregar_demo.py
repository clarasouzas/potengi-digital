from pathlib import Path

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Carrega os dados de demonstração do Potengi Digital."

    fixtures = (
        "cursos",
        "competencias",
        "areas",
        "empresas",
        "vagas",
        "noticias",
    )

    def handle(self, *args, **options):
        fixture_dir = Path(__file__).resolve().parents[3] / "fixtures"
        for fixture in self.fixtures:
            self.stdout.write(f"Carregando fixture {fixture}...")
            call_command("loaddata", str(fixture_dir / f"{fixture}.json"))
        self.stdout.write(self.style.SUCCESS("Dados de demonstração carregados."))
