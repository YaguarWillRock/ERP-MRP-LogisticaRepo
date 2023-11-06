# userInterface.py
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED, AlertDescription
from fastapi import FastAPI, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
from reactpy.backend.fastapi import configure
from reactpy import component, html
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import requests 

DATABASE_URL = "mysql+mysqlconnector://root@localhost/logistic"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    correo = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(255))
    fecha_registro = Column(DateTime, nullable=False)
    perfil_img = Column(String(255))

class SolicitudesEmbarque(Base):
    __tablename__ = 'SolicitudesEmbarque'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    fecha_entrega_estimada = Column(DateTime, nullable=False)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow) 
    fecha_recoleccion_estimada = Column(DateTime, nullable=True)  
    peso = Column(Numeric, nullable=False) 
    usuario_id = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)
    estado = Column(String(50), nullable=False, default='Pendiente') 

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/solicitar-embarque/")
async def solicitar_embarque(
    origen: str = Form(...),
    destino: str = Form(...),
    fecha_entrega_estimada: str = Form(...),
    peso: float = Form(...),  
    db: Session = Depends(get_db)
):
    
    if peso > 3000:
        return {"error": "El peso no puede exceder las 3 toneladas (3000 kg)"}

    fecha_entrega_estimada = datetime.strptime(fecha_entrega_estimada, "%Y-%m-%dT%H:%M")
    
    fecha_solicitud = datetime.utcnow()
    
    fecha_recoleccion_estimada = fecha_solicitud + timedelta(days=3)

    usuario_id = 1
    
    nueva_solicitud = SolicitudesEmbarque(
        origen=origen,
        destino=destino,
        fecha_entrega_estimada=fecha_entrega_estimada,
        fecha_solicitud=fecha_solicitud, 
        fecha_recoleccion_estimada=fecha_recoleccion_estimada, 
        usuario_id=usuario_id,
        estado="Pendiente",
        peso=peso
    )
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return {"message": "Solicitud de embarque creada", "solicitud_id": nueva_solicitud.id}

app.mount("/img", StaticFiles(directory="img"), name="images")
app.mount("/css", StaticFiles(directory="css"), name="css")

bootstrap_css = html.link({
    "rel": "stylesheet",
    "href": "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
})

font_awesome = html.link({
    "rel": "stylesheet",
    "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"
})

google_fonts = html.link({
    "href": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
    "rel": "stylesheet"
})

custom_css = html.link({
    "rel": "stylesheet",
    "href": "/css/styles.css"
})

@component
def UserInterface():
    def handle_submit(event):
        form_elements = event['currentTarget']['elements']
        event.preventDefault()
        origen = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['value'] != '' and "origen" in element['value'])
        destino = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['value'] != '' and "destino" in element['value'])
        fecha_entrega_estimada = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['value'] != '' and "fechaEntrega" in element['value'])


        response = requests.post(
            'http://localhost:8000/solicitar-embarque/',
            json={
                'origen': origen,
                'destino': destino,
                'fecha_entrega_estimada': fecha_entrega_estimada
            }
        )
        if response.ok:
            AlertDescription(response.json().get('message', 'Solicitud de embarque creada'))
        else:
            ALERT_DESCRIPTION_ACCESS_DENIED(response.json().get('error', 'Error desconocido'))
    return html.div(
        {
            "style": {
                "fontFamily": "'Roboto', sans-serif"
            }
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.header(
            {
                "className": "bg-primary text-white text-center p-3"
            },
            html.img({
                "src": "/img/logo_logistica.png",
                "alt": "Logo Logística",
                "style": {
                    "width": "50px",
                    "height": "50px"
                }
            }),
            html.h1("Logística"),
            html.span(
                {
                    "className": "fa fa-bell",
                    "style": {
                        "fontSize": "24px",
                        "float": "right",
                        "marginTop": "-40px",
                        "marginRight": "20px"
                    }
                }
            )
        ),
        html.main(
            {
                "className": "container mt-5"
            },
            html.div(
                {
                    "className": "mb-5"
                },
                html.h2("Solicitud de Embarque"),
                html.form(
                    {
                        "action": "/solicitar-embarque/",
                        "method": "post"
                    },
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "origen"}, "Origen:"),
                        html.input(
                            {
                                "type": "text",
                                "className": "form-control",
                                "name": "origen",
                                "placeholder": "Escriba el origen",
                                "required": True
                            }
                        )
                    ),
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "destino"}, "Destino:"),
                        html.input(
                            {
                                "type": "text",
                                "className": "form-control",
                                "name": "destino",
                                "placeholder": "Escriba el destino",
                                "required": True
                            }
                        )
                    ),
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "fecha_entrega_estimada"}, "Fecha de Entrega Requerida:"),
                        html.input(
                            {
                                "type": "datetime-local",
                                "className": "form-control",
                                "name": "fecha_entrega_estimada",
                                "required": True
                            }
                        )
                    ),
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "peso"}, "Peso (kg):"), 
                        html.input(
                            {
                                "type": "number",
                                "className": "form-control",
                                "name": "peso",
                                "placeholder": "Escriba el peso MENOR A 3000",
                                "required": True,
                                "step": "0.01" 
                            }
                        )
                    ),
                    html.button(
                        {
                            "type": "submit",
                            "className": "btn btn-primary"
                        },
                        "Enviar Solicitud"
                    )
                )
            ),
        ),
    )

configure(app, UserInterface)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)