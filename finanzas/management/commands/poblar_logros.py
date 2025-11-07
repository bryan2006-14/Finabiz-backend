from django.core.management.base import BaseCommand
from finanzas.models import TipoLogro

class Command(BaseCommand):
    help = 'Poblar la tabla tipos_logros con datos iniciales'

    def handle(self, *args, **options):
        tipos_logros = [
            {
                'nombre': 'Primer Gasto',
                'tipo': 'primer_gasto',
                'descripcion': 'Realiza tu primer gasto registrado',
                'icono': 'shopping-cart',
                'color': '#ef4444',
                'meta': 1
            },
            {
                'nombre': 'Primer Ingreso',
                'tipo': 'primer_ingreso', 
                'descripcion': 'Registra tu primer ingreso',
                'icono': 'dollar-sign',
                'color': '#10b981',
                'meta': 1
            },
            {
                'nombre': 'Control de Gastos',
                'tipo': 'gasto_mensual',
                'descripcion': 'Mantén tus gastos mensuales por debajo de tu meta',
                'icono': 'trending-down',
                'color': '#f59e0b',
                'meta': 1000
            },
            {
                'nombre': 'Ahorrador Mensual',
                'tipo': 'ahorro_mensual',
                'descripcion': 'Ahorra más de $500 en un mes',
                'icono': 'piggy-bank',
                'color': '#06b6d4',
                'meta': 500
            },
            {
                'nombre': 'Consistencia Financiera',
                'tipo': 'consistencia',
                'descripcion': 'Registra transacciones por 7 días consecutivos',
                'icono': 'calendar',
                'color': '#8b5cf6',
                'meta': 7
            },
            {
                'nombre': 'Meta de Ahorro',
                'tipo': 'meta_ahorro',
                'descripcion': 'Alcanza tu primera meta de ahorro de $1000',
                'icono': 'target',
                'color': '#4f46e5',
                'meta': 1000
            },
        ]

        for logro_data in tipos_logros:
            tipo_logro, created = TipoLogro.objects.get_or_create(
                tipo=logro_data['tipo'],
                defaults=logro_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Creado: {logro_data["nombre"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Ya existe: {logro_data["nombre"]}')
                )