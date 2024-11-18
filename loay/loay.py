import streamlit as st
import pandas as pd

# Título de la página y introducción
st.title("🚗 Explora La Ruta de las Kasbahs en Marruecos")
# st.write("""
# La **Ruta de las Kasbahs** es un famoso camino en Marruecos que conecta Marrakech con Ouarzazate. A lo largo de esta ruta, experimentarás las maravillas arquitectónicas bereberes, como las kasbahs, y los impresionantes paisajes de las montañas del Atlas, desiertos y oasis verdes.
# """)

# Barra lateral para la navegación
st.sidebar.title("🧭 Navegación")
st.sidebar.write("Explora las diferentes secciones sobre La Ruta de las Kasbahs:")
section = st.sidebar.radio("Selecciona una sección", ("Descripción General", "Geografía y Paisaje", "Mapa Interactivo"))

# Sección 1: Descripción General
if section == "Descripción General":
    # st.header("Acerca de la Ruta")
    st.write("""
    La *Ruta de las Kasbahs* es un camino famoso en Marruecos que conecta Marrakech con Ouarzazate. Cruza paisajes desérticos impresionantes y muestra una arquitectura bereber única, con kasbahs de tierra. Un lugar importante es *Aït Ben Haddou, con sus casas de tierra roja y decoraciones geométricas. Otra es la **Kasbah de Taourirt* en Ouarzazate, que muestra la habilidad bereber con sus muros gruesos y su resistencia al clima seco. La Ruta de las Kasbahs es una experiencia cultural que permite conocer la historia y la vida tradicional de los bereberes.

    """)
    st.image("/workspaces/Dashboard-pronote/loay/1.jpeg", caption="Aït Ben Haddou")

    st.subheader("Significado Histórico y Cultural")
    st.write("""
   El paisaje a lo largo de esta ruta es impresionante, con montañas del Atlas y grandes extensiones de desierto. Se pueden ver oasis verdes y palmeras. Los colores rojos y ocres predominan y se mezclan con montañas y cañones profundos, como el del Dadès. A veces, ríos fluyen en estos desiertos secos y crean pequeñas valles fértiles donde crecen olivos, almendros y rosas silvestres. El contraste entre el desierto y los oasis tranquilos muestra un lugar antiguo, donde el tiempo se siente en cada piedra y cada kasbah.
    """)

# Sección 3: Geografía y Paisaje
elif section == "Geografía y Paisaje":
    st.header("🗺️ Geografía y Paisaje")
    st.write("""
    Geographia:
Para ir de Marrakech a Ouarzazate se recomienda tomar el coche aunque sea 3 horas y media de trayecto porque vas a encontrarte con vistas increíbles. La ruta es muy tranquila pero no hay autopista entonces no vas muy rápido pero vas a ser impresionado con las vistas increíbles porque tienes que pasar por las montañas tizi tin’Tchka que son muy chulas. Luego pasarás por un desierto muy seco con colinas alrededor antes de llegar a Ouarzazate.
    """)
    
    # Detalles del Paisaje
    st.subheader("Actividades")
    st.write("""
    En Ouarzazate se recomienda visitar El museo de cinematografía de Ouarzazate y también Atlas Studios para ver cómo son realmente los paisajes de una película. Luego puedes Visitar la Kasbah de Taourirt que es muy bonita. Luego si te gusta más hacer actividades con más acción puedes hacer un viaje con un quad o un buggy en el desierto de Ouarzazate que te va a llevar a un oasis antes de volver. Si esto no es suficiente y no te molesta hacer más ruta puedes ir a Merzouga para hacer camello en el desierto de Merzouga y dormir ahí.
    """)
    st.image("/workspaces/Dashboard-pronote/loay/2.jpeg", caption="Paisaje Desértico a lo largo de la Ruta")
    st.image("/workspaces/Dashboard-pronote/loay/3.jpeg")

# Sección 4: Mapa Interactivo con Detalles Geográficos
elif section == "Mapa Interactivo":
    st.header("📍 Mapa Interactivo de La Ruta de las Kasbahs")
    st.write("Explora La Ruta de las Kasbahs interactivamente en el mapa a continuación.")

    # Datos para los puntos del mapa
    map_data = pd.DataFrame({
        'lat': [31.047, 30.926, 31.533],
        'lon': [-7.130, -6.910, -5.920],
        'name': ["Aït Ben Haddou", "Kasbah de Taourirt", "Cañón del Dadès"]
    })
    
    # Mostrar el mapa con los puntos
    st.map(map_data)
