import urllib.parse
import plotly.graph_objects as go
import streamlit as st

from tessuto import ScartoTessile

st.set_page_config(
    page_title="DSS Riciclo Tessile", # Cambia anche il nome nella scheda del browser
    page_icon= "♻️",
    layout="wide" # ALLARGA LA PAGINA
)

# Rimuove lo spazio vuoto ad inizio pagina
st.markdown("""
    <style>
    # Aumentato da 1rem a 3rem per non tagliare il titolo
    # Spazio sotto maggiore
               .block-container {
                    padding-top: 3rem;  
                    padding-bottom: 1rem; 
                }
    </style>
    """, unsafe_allow_html=True)

#==============================
#           SIDEBAR
#==============================
# --- LOCALIZZAZIONE UTENTE ---
st.sidebar.header("🌍 Localizzazione Utente")

nazioni_origine = {
    "Svizzera (Ticino)": [46.0037, 8.9511],
    "Italia (Nord)": [45.4642, 9.1900],
    "Germania": [51.1657, 10.4515],
    "Belgio": [50.8503, 4.3517],
    "Paesi Bassi": [52.1326, 5.2913],
    "Francia": [48.8566, 2.3522],
    "Spagna": [40.4168, -3.7038],
    "Austria": [48.2082, 16.3738]
}

nazione_scelta = st.sidebar.selectbox("In quale nazione si trova il tuo lotto?", list(nazioni_origine.keys()))
lat_partenza, lon_partenza = nazioni_origine[nazione_scelta]

# NUOVA CHECKBOX NORMATIVA

st.sidebar.markdown("### ⚖️ Compliance Normativa")
is_green_list = st.sidebar.checkbox(
    "Il lotto appartiene alla 'Green List' UE?",
    value=True,
    help="Se deselezionato, le normative doganali impongono il trattamento all'interno dei confini nazionali (New Regulation on waste shipments)."
)

tipo_trasporto = st.sidebar.selectbox("Mezzo di Trasporto Logistico", ["Camion", "Treno", "Nave"])


# 3. Destinazione Finale (Brand e Poli Logistici per la vendita)
destinazioni_finali = {
    "Mango (Barcellona, Spagna)": [41.3851, 2.1734],
    "Bobo Choses (Mataró, Spagna)": [41.5381, 2.4445],
    "Decathlon (Lilla, Francia)": [50.6292, 3.1360],
    "C&A (Düsseldorf, Germania)": [51.2277, 6.7735],
    "Sioen Industries (Ardooie, Belgio)": [50.9757, 3.1996],
    "Marks & Spencer (Londra, UK)": [51.5074, -0.1278],
    "H&M (Stoccolma, Svezia)": [59.3293, 18.0686],
    "Pusu Skis (Jyväskylä, Finlandia)": [62.2415, 25.7209]
}
destinazione_scelta = st.sidebar.selectbox("Destinazione Prodotto Finito (Brand):", list(destinazioni_finali.keys()))
lat_arrivo, lon_arrivo = destinazioni_finali[destinazione_scelta]

# st.sidebar.divider()
st.sidebar.markdown(
    "<hr style='margin-top: 10px; margin-bottom: 5px; border: 0; border-top: 1px solid rgba(255,255,255,0.2);'>"
    "<h3 style='margin-top: 0px; padding-top: 0px;",
    unsafe_allow_html=True
)

# --- PARAMETRI TESSUTO ---
st.sidebar.header("Parametri Tessuto")

presets = {
    "Policotone (Cotone + Poliestere)": [65, 35, 0, 0, 0, 0],
    "TripleBlend (Cotone + Poliestere + Elastan)": [60, 35, 5, 0, 0, 0], # Corretto: 5 valori
    "Lana e Acrilico": [0, 0, 0, 50, 50, 0],
    "Nylon ed Elastane": [0, 0, 15, 0, 0, 85],
    "Altro (Manuale)": [20, 20, 10, 20, 15, 15]
}

nome_lotto = st.sidebar.selectbox("Seleziona il tipo di materiale", list(presets.keys()))
val_c, val_p, val_e, val_l, val_a, val_n = presets[nome_lotto]

c = st.sidebar.slider("Cotone %", 0, 100, val_c)
p = st.sidebar.slider("Poliestere %", 0, 100, val_p)
e = st.sidebar.slider("Elastan %", 0, 100, val_e)
l = st.sidebar.slider("Lana %", 0, 100, val_l)
a = st.sidebar.slider("Acrilico %", 0, 100, val_a)
n = st.sidebar.slider("Nylon %", 0, 100, val_n)

somma_totale = c + p + e + l + a + n
if somma_totale != 100:
    st.sidebar.warning(f"Attenzione: La somma è {somma_totale}% invece di 100%.")

# --- LOGICA ---
mio_scarto = ScartoTessile(nome_lotto, c, p, e, l, a, n)
percorso, spiegazione = mio_scarto.calcola_riciclo()
co2 = mio_scarto.kpi_ambientale()

# Estraiamo il nome del paese di origine "puro" togliendo parentesi (es. da "Svizzera (Ticino)" a "Svizzera")
paese_origine_puro = nazione_scelta.split(" (")[0].strip()

# Passiamo anche la nazione pura e la variabile is_green_list al motore di ricerca
lista_attori = mio_scarto.get_partner_specializzati(
    lat_origine=lat_partenza,
    lon_origine=lon_partenza,
    is_green_list=is_green_list,       # Passiamo la spunta
    paese_origine=paese_origine_puro,  # Passiamo il paese
    tipo_trasporto=tipo_trasporto,
    tecnica_suggerita=percorso
)

#==============================
#       PAGINA CENTRALE
#==============================

# --- VISUALIZZAZIONE RISULTATI ---

# Due colonne per logo e titolo
col_logo, col_titolo = st.columns([1, 7])

# Inserimento logo
#with col_logo:
    st.image("logo.jpg", width=120)

# Inserimento Titolo
with col_titolo:
    st.title("Super Fiber Tool")

# st.subheader("Super Fiber Tool")
st.subheader(f"Analisi per: {nome_lotto}")

# --- CREAZIONE DELLE TAB PER UN LAYOUT PIÙ PULITO ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & KPI", "🌍 Mappa Supply Chain", "🏷️ Passaporto Digitale"])


# ==========================================
# TAB 1: ANALISI DECISIONALE E KPI (RADAR & PIE)
# ==========================================
with tab1:
    #st.write(f"Analisi per: {nome_lotto}")
    st.markdown(f"#### Processo Suggerito: {percorso}")

    # Visualizza la spiegazione dentro un box informativo azzurro
    st.info(spiegazione)

    st.divider()

    # Recuperiamo il dizionario con i dati corretti dal tuo oggetto tessuto
    dati_kpi = mio_scarto.kpi_ambientale()

    st.write("### KPI (Risparmio con Riciclo rispetto al prodotto nuovo)")
    col_env1, col_env2, col_env3, col_env4, col_env5 = st.columns(5)

    with col_env1:
        st.metric(label="Emissioni di CO₂", value=dati_kpi["co2"], help=dati_kpi["note_co2"])

    with col_env2:
        st.metric(label="Consumo di Acqua", value=dati_kpi["acqua"], help=dati_kpi["note_acqua"])

    with col_env3:
        st.metric(label="Energia Richiesta", value=dati_kpi["energia"], help=dati_kpi["note_energia"])

    with col_env4:
        st.metric(label="Uso del Suolo", value=dati_kpi["suolo"], help=dati_kpi["note_suolo"])

    with col_env5:
        st.metric(label="Affidabilità (1-5)", value=dati_kpi.get("affidabilità", "5"),
                  help="Qualità del dato basata su fonti verificate")

    st.divider()

    # --- GRAFICI (PIE & RADAR) ---
    st.write("### Analisi Visiva Composizione e Sostenibilità")

    # Creiamo due colonne per affiancare i grafici
    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:

        # 1. GRAFICO A TORTA (COMPOSIZIONE)
        labels = ['Cotone', 'Poliestere', 'Elastan', 'Lana', 'Acrilico', 'Nylon']
        values = [c, p, e, l, a, n]

        # Filtriamo per nascondere i materiali allo 0% dal grafico
        labels_filtered = [label for label, value in zip(labels, values) if value > 0]
        values_filtered = [value for value in values if value > 0]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels_filtered,
            values=values_filtered,
            hole=.4,  # Questo parametro lo fa diventare una ciambella!
            marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        )])

        fig_pie.update_layout(
            title_text="Composizione del Lotto",
            margin=dict(t=40, b=10, l=10, r=10),
            height=360,
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_grafico2:
        # 2. GRAFICO RADAR (CIRCOLARITÀ AI)
        import re

        # Piccola funzione per estrarre i numeri dalle stringhe dei KPI (es. "-30-40%" -> 40)
        def estrai_numero(testo):
            numeri = re.findall(r'\d+', testo)
            return int(numeri[-1]) if numeri else 50


        score_co2 = estrai_numero(dati_kpi["co2"])
        score_acqua = estrai_numero(dati_kpi["acqua"])
        score_energia = estrai_numero(dati_kpi["energia"])

        # Calcoliamo una "Riciclabilità" in base ai materiali ostici come l'Elastan
        # Nuova formula con penalità anche per il poliestere (p)
        # Se p=35 ed e=0, l'indice scenderà a 100 - (35 * 0.5) = 82.5%
        riciclabilita = max(10, 100 - (p * 0.5) - (e * 3.5) - (n * 1.5))
        circolarita = (score_co2 + score_acqua + score_energia + riciclabilita) / 4

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[riciclabilita, score_co2, score_acqua, score_energia, circolarita],
            theta=['Riciclabilità Base', 'Risparmio CO₂', 'Risparmio Idrico', 'Effic. Energetica',
                   'Indice Circolarità'],
            fill='toself',
            name='Punteggio',
            line_color='#17becf'
        ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title_text="Profilo di Sostenibilità",
            margin=dict(t=40, b=10, l=40, r=40),
            height=360,
            paper_bgcolor='rgba(0,0,0,0)',
            dragmode=False,

        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})


# ==========================================
# TAB 2: MAPPA E LOGISTICA
# ==========================================
    with tab2:
        st.subheader("Tracciabilità della Filiera e Distanze")

        # L'algoritmo in tessuto.py ha già restituito la lista ordinata per MINOR CO2 TOTALE
        if lista_attori:

            # Separiamo le aziende in base al ruolo reale (leggendo il campo 'tecnica')
            sorters = [a for a in lista_attori if a["tecnica"] == "Raccolta e sorting"]
            riciclatori = [a for a in lista_attori if a["tecnica"] != "Raccolta e sorting"]

            if sorters and riciclatori:
                best_sorter = sorters[0]
                best_riciclatore = riciclatori[0]

                # Usiamo le coordinate scelte dalla sidebar
                brand_finale = {"nome": destinazione_scelta, "lat": lat_arrivo, "lon": lon_arrivo}

                # --- CALCOLO KM TOTALI DEL PROCESSO ---
                km1 = mio_scarto.calcola_distanza(lat_partenza, lon_partenza, best_sorter["lat"], best_sorter["lon"])
                km2 = mio_scarto.calcola_distanza(best_sorter["lat"], best_sorter["lon"], best_riciclatore["lat"],
                                                  best_riciclatore["lon"])
                km3 = mio_scarto.calcola_distanza(best_riciclatore["lat"], best_riciclatore["lon"], brand_finale["lat"],
                                                  brand_finale["lon"])
                km_totali = km1 + km2 + km3

                # --- CREAZIONE MAPPA ---
                lats_percorso = [lat_partenza, best_sorter["lat"], best_riciclatore["lat"], brand_finale["lat"]]
                lons_percorso = [lon_partenza, best_sorter["lon"], best_riciclatore["lon"], brand_finale["lon"]]

                fig_map = go.Figure()

                # Linea del percorso
                fig_map.add_trace(go.Scattermapbox(
                    mode='lines', lat=lats_percorso, lon=lons_percorso,
                    line=dict(width=3, color='rgba(0, 123, 255, 0.8)'),
                    name="Flusso Materiale"
                ))

                # Punti della filiera
                colori_tappe = ['red', 'orange', 'green', 'purple']
                nomi_tappe = ['Origine', 'Smistamento', 'Riciclo', 'Nuovo Prodotto']

                for i in range(len(lats_percorso)):
                    fig_map.add_trace(go.Scattermapbox(
                        lat=[lats_percorso[i]], lon=[lons_percorso[i]],
                        mode='markers',
                        marker=go.scattermapbox.Marker(size=14, color=colori_tappe[i]),
                        name=nomi_tappe[i], hovertext=nomi_tappe[i]
                    ))

                # --- CALCOLO CENTRO E ZOOM ADATTIVO ---
                # (Spostato FUORI dal ciclo for per non sovrascrivere il layout)
                centro_lat = sum(lats_percorso) / len(lats_percorso)
                centro_lon = sum(lons_percorso) / len(lons_percorso)

                diff_lat = max(lats_percorso) - min(lats_percorso)
                diff_lon = max(lons_percorso) - min(lons_percorso)
                diff_max = max(diff_lat, diff_lon)

                if diff_max > 15:
                    zoom_dinamico = 2.8
                elif diff_max > 10:
                    zoom_dinamico = 3.5
                elif diff_max > 5:
                    zoom_dinamico = 4.5
                else:
                    zoom_dinamico = 5.5

                # --- STILE MAPPA E LEGENDA ---
                fig_map.update_layout(
                    mapbox_style="open-street-map",
                    mapbox=dict(
                        center=dict(lat=centro_lat, lon=centro_lon),
                        zoom=zoom_dinamico
                    ),
                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    height=600, showlegend=True,
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255, 255, 255, 0.8)",
                                font=dict(color="black"))
                )

                st.plotly_chart(fig_map, use_container_width=True)

                # --- MESSAGGI DI OTTIMIZZAZIONE E DOGANA ---
                nazione_sorter = best_sorter.get('nazione', 'Europa')
                nazione_riciclo = best_riciclatore.get('nazione', 'Europa')

                # Se la Green List è disattivata, mostriamo l'avviso di "Filiera Chiusa"
                if not is_green_list:
                    st.warning(
                        f"🔒 **Vincolo Doganale Attivo:** Il lotto non appartiene alla *Green List*. La filiera (Smistamento e Riciclo) è stata forzata all'interno dei confini di origine ({paese_origine_puro}) prima dell'esportazione del prodotto finito verso il Brand.")

                st.success(
                    f"**Ottimizzazione Algoritmo (LCA):** Smistamento a **{best_sorter['nome']}** ({nazione_sorter}) e riciclo presso **{best_riciclatore['nome']}** ({nazione_riciclo}).")

                # Calcolo totali emissioni
                co2_logistica = best_sorter["co2_trasporto"] + best_riciclatore["co2_trasporto"]
                co2_energia = best_sorter["co2_processo"] + best_riciclatore["co2_processo"]
                co2_assoluta = best_sorter["co2_totale"] + best_riciclatore["co2_totale"]

                st.info(
                    f"**Logistica ({tipo_trasporto}):** {int(km_totali)} km ({co2_logistica:.1f} kg CO₂/ton) ⸺ **Energia Processo:** {co2_energia:.1f} kg CO₂/ton")
                st.write(
                    f"Il sistema ha bilanciato i consumi del **{tipo_trasporto}** con il mix energetico nazionale, contenendo le emissioni totali a **{co2_assoluta:.1f} kg di CO₂ / ton**.")

            else:
                # Errore specifico se mancano aziende nazionali a causa del blocco doganale
                if not is_green_list:
                    st.error(
                        f"❌ **Blocco Doganale (End-of-Waste):** Impossibile chiudere la filiera. Mancano impianti autorizzati e compatibili con questo materiale in **{paese_origine_puro}**. Spunta 'Green List UE' per esportare il rifiuto e trovare partner esteri.")
                else:
                    st.warning("Database incompleto per creare una filiera per questo materiale.")
        else:
            if not is_green_list:
                st.error(
                    f"❌ **Blocco Doganale (End-of-Waste):** Impossibile chiudere la filiera in **{paese_origine_puro}**.")
            else:
                st.warning("Nessuna azienda compatibile trovata.")




# ==========================================
# TAB 3: PASSAPORTO DIGITALE (DPP)
# ==========================================

with tab3:
    st.header("Digital Product Passport (DPP)")
    st.markdown(
        "Simulazione del passaporto digitale conforme alle direttive ESPR per la tracciabilità end-to-end e l'integrazione con i sistemi di sorting 4.0 (sensori NIR).")

    import uuid
    import urllib.parse
    import plotly.graph_objects as go

    # Generiamo un ID univoco simulato per il lotto (stile Certilogo/EON)
    uid_capo = f"TX-2026-{str(uuid.uuid4())[:6].upper()}"

    col_a, col_b = st.columns([1, 1])

    with col_a:
        # 1. IDENTITÀ DIGITALE
        with st.expander("Identità Digitale e Autenticità", expanded=True):
            st.markdown(f"**UID Prodotto:** `{uid_capo}`")
            st.markdown(f"**Paese di Origine:** {nazione_scelta}")
            st.markdown(f"**Brand di Destinazione:** {destinazione_scelta}")
            st.markdown("**Data di Immissione:** 2026")
            st.markdown("**Status:** 🟢 Verificato (Blockchain/Anti-contraffazione)")

        # 2. DATI TECNICI PER MACCHINARI (NIR)
        with st.expander("Dati Tecnici per Sorting 4.0 (Cloud EON)"):
            st.markdown("**Composizione Rilevata dal Sensore Ottico:**")
            st.write(f"- Cotone: {c}%\n- Poliestere: {p}%\n- Elastan: {e}%\n- Lana: {l}%\n- Acrilico: {n}%")

            # Simulazione di lettura dei contaminanti
            if e > 0:
                st.warning(
                    "Allerta Sensori: Rilevata presenza di contaminanti poliuretanici (Elastan). Deviare verso sfilacciatura.")
            elif n > 0:
                st.warning("Allerta Sensori: Acrilico rilevato. Applicare finissaggi antistatici in lavorazione.")
            else:
                st.success("Fibra cellulosica/proteica pura: idonea a processi chimici/enzimatici a ciclo chiuso.")

        # 3. IMPRONTA AMBIENTALE
        with st.expander("Impronta Ambientale e LCA"):
            st.markdown(f"**Risparmio CO₂ (vs Vergine):** {co2['co2']}")
            st.markdown(f"**Risparmio Idrico:** {co2['acqua']}")
            st.markdown(f"**Affidabilità Dato (TRL):** {co2['affidabilità']} / 5")

        # 4. CIRCOLARITÀ E QR CODE
        with st.expander("Istruzioni di Circolarità ed Esportazione"):
            st.markdown(f"**Tecnologia Designata:** {percorso}")

            # Creazione Link per QR Code (Mailto simulata)
            oggetto = urllib.parse.quote(f"Manifesto di Carico - {uid_capo}")
            corpo = urllib.parse.quote(
                f"Trasmissione dati Passaporto Digitale.\nUID: {uid_capo}\nDestinazione: {destinazione_scelta}\nTecnologia: {percorso}")
            mailto_link = f"mailto:compliance@hub-circolare.eu?subject={oggetto}&body={corpo}"

            # Generazione QR Code tramite API gratuita
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={mailto_link}"

            col_qr1, col_qr2 = st.columns([1, 2])
            with col_qr1:
                st.image(qr_url, width=120)
            with col_qr2:
                st.markdown(
                    "**Scansiona il QR Code** per trasmettere istantaneamente i dati di conformità al gestionale dell'impianto di smaltimento.")

    with col_b:
        st.markdown("### Flusso Termodinamico (Sankey)")
        st.markdown("Rappresentazione delle rese e degli scarti fisici durante il trattamento industriale.")

        # Parametri logici dinamici in base alla tecnologia scelta dall'AI
        if "Chimico" in percorso:
            resa = 85
            scarto = 15
            nome_scarto = "Solventi esausti / Decolorazione"
            colore_flusso = "#17a2b8"  # Azzurro chimica
        elif "Meccanico" in percorso:
            resa = 70
            scarto = 30
            nome_scarto = "Polvere / Fibre Corte (Downcycling)"
            colore_flusso = "#6c757d"  # Grigio meccanica
        else:
            resa = 90
            scarto = 10
            nome_scarto = "Scarto Biologico (Biomassa)"
            colore_flusso = "#28a745"  # Verde biotech

        # Creazione Diagramma di Sankey con Plotly
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=25,
                line=dict(color="black", width=0.5),
                label=["Lotto Ingresso (100%)", "Impianto di Riciclo", f"Fibra Rigenerata ({resa}%)",
                       f"{nome_scarto} ({scarto}%)"],
                color=["#007bff", colore_flusso, "#28a745", "#dc3545"]
            ),
            link=dict(
                source=[0, 1, 1],  # Indici dei nodi di partenza
                target=[1, 2, 3],  # Indici dei nodi di arrivo
                value=[100, resa, scarto],  # Quantità trasferite
                color=["rgba(0, 123, 255, 0.3)", "rgba(40, 167, 69, 0.4)", "rgba(220, 53, 69, 0.4)"]
            ))])

        fig_sankey.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_sankey, use_container_width=True)
