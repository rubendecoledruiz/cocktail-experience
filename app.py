import csv
import os
import re
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
RESERVATIONS_FILE = Path(
    os.environ.get("RESERVATIONS_FILE", BASE_DIR / "instance" / "reservas.csv")
)

FORMATS = {
    "dos": "Cocktail Experience para Dos",
    "friends": "Cocktail Experience Friends",
    "autor": "Experiencia de Autor",
    "no-se": "Aún no lo sé",
}

PREFERENCES = {
    "Clásicos",
    "Frutales y frescos",
    "Cítricos y herbales",
    "Me gustan las sorpresas",
    "Sin alcohol o mixtos",
}

CSV_FIELDS = [
    "fecha_solicitud",
    "nombre",
    "whatsapp",
    "email",
    "fecha_deseada",
    "localidad",
    "personas",
    "formato",
    "preferencias",
    "mensaje",
]


def safe_csv_value(value: str) -> str:
    """Prevent spreadsheet applications from interpreting submitted text as a formula."""
    if value.startswith(("=", "+", "-", "@", "\t", "\r")):
        return f"'{value}"
    return value


def save_reservation(reservation: dict[str, str]) -> None:
    RESERVATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not RESERVATIONS_FILE.exists() or RESERVATIONS_FILE.stat().st_size == 0

    encoding = "utf-8-sig" if needs_header else "utf-8"
    with RESERVATIONS_FILE.open("a", newline="", encoding=encoding) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow({key: safe_csv_value(value) for key, value in reservation.items()})


@app.get("/")
def home():
    whatsapp_number = re.sub(
        r"\D", "", os.environ.get("WHATSAPP_NUMBER", "+34 632 985 492")
    )
    return render_template(
        "index.html",
        whatsapp_number=whatsapp_number,
        contact_email=os.environ.get("CONTACT_EMAIL", "lovecocteleria@gmail.com"),
    )


@app.post("/reservar")
def reserve():
    data = request.get_json(silent=True) or request.form

    # Honeypot field: real visitors leave this hidden input empty.
    if data.get("website", "").strip():
        return jsonify(ok=True, message="Gracias. Hemos recibido tu solicitud."), 200

    required_fields = (
        "nombre",
        "whatsapp",
        "email",
        "fecha",
        "localidad",
        "personas",
        "formato",
        "preferencias",
    )
    values = {field: str(data.get(field, "")).strip() for field in required_fields}
    values["mensaje"] = str(data.get("mensaje", "")).strip()

    if any(not values[field] for field in required_fields):
        return jsonify(ok=False, message="Revisa los campos obligatorios."), 400
    if len(values["nombre"]) > 100 or len(values["localidad"]) > 100:
        return jsonify(ok=False, message="El nombre o la localidad son demasiado largos."), 400
    if len(values["whatsapp"]) > 30 or len(values["email"]) > 254:
        return jsonify(ok=False, message="Revisa el teléfono o el email introducido."), 400
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", values["email"]):
        return jsonify(ok=False, message="Introduce un email válido."), 400
    if values["formato"] not in FORMATS:
        return jsonify(ok=False, message="Selecciona uno de los formatos disponibles."), 400
    if values["preferencias"] not in PREFERENCES:
        return jsonify(ok=False, message="Selecciona una preferencia de cócteles válida."), 400

    try:
        people = int(values["personas"])
    except ValueError:
        return jsonify(ok=False, message="El número de personas no es válido."), 400
    if not 2 <= people <= 6:
        return jsonify(ok=False, message="La experiencia está pensada para grupos de 2 a 6 personas."), 400
    try:
        desired_date = datetime.strptime(values["fecha"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify(ok=False, message="Introduce una fecha válida."), 400
    if desired_date < datetime.now().astimezone().date():
        return jsonify(ok=False, message="La fecha deseada no puede estar en el pasado."), 400
    if len(values["preferencias"]) > 150 or len(values["mensaje"]) > 2000:
        return jsonify(ok=False, message="El mensaje supera la longitud permitida."), 400

    reservation = {
        "fecha_solicitud": datetime.now().astimezone().isoformat(timespec="seconds"),
        "nombre": values["nombre"],
        "whatsapp": values["whatsapp"],
        "email": values["email"],
        "fecha_deseada": values["fecha"],
        "localidad": values["localidad"],
        "personas": str(people),
        "formato": FORMATS[values["formato"]],
        "preferencias": values["preferencias"],
        "mensaje": values["mensaje"],
    }

    try:
        save_reservation(reservation)
    except OSError:
        app.logger.exception("No se pudo guardar la solicitud de reserva.")
        return (
            jsonify(
                ok=False,
                message="No se pudo guardar tu solicitud. Prueba de nuevo o contacta directamente.",
            ),
            500,
        )

    return jsonify(
        ok=True,
        message="¡Gracias! Tu solicitud está guardada. Rubén se pondrá en contacto contigo para confirmar disponibilidad.",
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
