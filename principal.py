from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy.backend.fastapi import configure
from reactpy import component, html

app = FastAPI()

app.mount("/img", StaticFiles(directory="img"), name="images")
app.mount("/css", StaticFiles(directory="css"), name="css")

# estilos y otras cosillas
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

@component
def Dashboard():
    return html.div(
        {
            "style": {
                "backgroundImage": "url('/img/3.png')",
                "backgroundSize": "cover",
                "backgroundRepeat": "no-repeat"
            }
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        html.div({"className": "container mt-5"},  
            html.div({"className": "text-center mb-4"},
                html.img({
                    "src": "/img/logo_logistica.png",
                    "alt": "Logo de la Empresa",
                    "width": 150
                })
            ),
            html.div({"className": "card mb-4"},
                html.div({"className": "card-header"},
                    html.h4("Entregas y Recogidas Pendientes")
                ),
                html.div({"className": "card-body"},
                    html.ul(
                        html.li("Entrega para el Cliente A - 05/10/2023"),
                        html.li("Recogida en Almacén B - 06/10/2023")
                    )
                )
            ),
            html.div({"className": "card mb-4"},
                html.div({"className": "card-header"},
                    html.h4("Notificaciones y Alertas")
                ),
                html.div({"className": "card-body"},
                    html.ul(
                        html.li("El Proveedor X ha confirmado la entrega para el 10/10/2023."),
                        html.li("Alerta: Bajo inventario de Producto Z.")
                    )
                )
            ),
            html.div({"className": "card"},
                html.div({"className": "card-header"},
                    html.h4("Accesos Directos")
                ),
                html.div({"className": "card-body"},
                    html.div({"className": "row"},
                        html.div({"className": "col-md-4 text-center"},
                            html.a({
                                "href": "#",
                                "className": "btn btn-outline-primary btn-lg mb-3"
                            },
                                html.i({"className": "fas fa-truck"}),
                                html.br(),
                                "Gestionar Rutas"
                            )
                        ),
                        # html.div({"className": "col-md-4 text-center"},
                        #     html.a({
                        #         "href": "#",
                        #         "className": "btn btn-outline-primary btn-lg mb-3"
                        #     },
                        #         html.i({"className": "fas fa-boxes"}),
                        #         html.br(),
                        #         "Inventario"
                        #     )
                        # ),
                        html.div({"className": "col-md-4 text-center"},
                            html.a({
                                "href": "#",
                                "className": "btn btn-outline-primary btn-lg mb-3"
                            },
                                html.i({"className": "fas fa-users"}),
                                html.br(),
                                "Clientes"
                            )
                        )
                    )
                )
            )
        )
    )

configure(app, Dashboard)


# # app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/img", StaticFiles(directory="img"), name="3")
# app.mount("/css", StaticFiles(directory="css"), name="css")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
