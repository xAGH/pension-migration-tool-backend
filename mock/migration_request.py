import csv
import random
from datetime import date, timedelta

from faker import Faker

fake = Faker("es_CO")  # Faker with Colombian localization

# Constants
CITIES = [
    "Medellín",
    "Bogotá",
    "Cali",
    "Cartagena",
    "Bucaramanga",
    "Manizales",
    "Sultán",
    "Quintán",
]
INSTITUTIONS = ["Armada", "Inpec", "Policia", "Minsalud", "Mininterior"]
PENSION_FUNDS = [
    "Porvenir",
    "Proteccion",
    "Colfondos",
    "Old Mutual",
    "Fondo Extranjero",
]


def random_date(start, end):
    """Generate a random date between `start` and `end`."""
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_person():
    """Generate a dictionary with a person's details."""
    institucion_publica = random.choice(
        INSTITUTIONS + [None, None, None]
    )  # Make institutions more rare
    tiene_hijos = random.choice([True, False])
    return {
        "identificacion": fake.unique.random_int(min=1_000_000_000, max=9_999_999_999),
        "primer_nombre": fake.first_name(),
        "segundo_nombre": random.choice([fake.first_name(), None]),
        "primer_apellido": fake.last_name(),
        "segundo_apellido": random.choice([fake.last_name(), None]),
        "genero": random.choice(["M", "H"]),
        "fecha_de_nacimiento": random_date(
            date(1950, 1, 1), date(2002, 12, 31)
        ).isoformat(),
        "ciudad_de_residencia": random.choice(CITIES),
        "ciudad_de_nacimiento": fake.city(),
        "semanas_cotizadas": random.randint(0, 2500),
        "fondo_actual": random.choice(PENSION_FUNDS),
        "pre_pensionado": random.choice([True, False]),
        "institucion_publica": institucion_publica,
        "numero_hijos": random.randint(0, 5) if tiene_hijos else 0,
        "condecoracion": random.choice([True, False]),
        "tiene_hijos_inpec": tiene_hijos and institucion_publica == "Inpec",
        "tiene_familia_policia": institucion_publica == "Policia",
        "observaciones_disciplinarias": random.choice(
            [
                fake.sentence(),
                None,
                None,
                None,
            ]
        ),
    }


def generate_csv(filename, num_records):
    """Generate a CSV file with `num_records` Person data."""
    fieldnames = [
        "identificacion",
        "primer_nombre",
        "segundo_nombre",
        "primer_apellido",
        "segundo_apellido",
        "genero",
        "fecha_de_nacimiento",
        "ciudad_de_residencia",
        "ciudad_de_nacimiento",
        "semanas_cotizadas",
        "fondo_actual",
        "pre_pensionado",
        "institucion_publica",
        "numero_hijos",
        "condecoracion",
        "tiene_hijos_inpec",
        "tiene_familia_policia",
        "observaciones_disciplinarias",
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(num_records):
            writer.writerow(generate_person())
