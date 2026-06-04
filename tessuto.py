
import math

class ScartoTessile:
    """Questa è la tua classe base, come in Java"""


    def __init__(self, nome, cotone, poliestere, elastan, lana=0, nylon=0, acrilico=0):
        self.nome = nome
        self.cotone = cotone
        self.poliestere = poliestere
        self.elastan = elastan
        self.lana = lana
        self.nylon = nylon
        self.acrilico = acrilico

    def calcola_riciclo(self):
        """Metodo per decidere il percorso (Logica decisionale)"""

        # 1. Combinazione Nylon + Elastan (Activewear / Swimwear)
        if self.nylon > 0 and self.elastan > 0:
            return "🔴 Riciclo Meccanico", (
                "I blend di Nylon ed Elastan (tipici dell'abbigliamento sportivo) sono estremamente difficili da separare chimicamente. "
                "L'Elastan si comporta come un contaminante gommoso che degrada i solventi necessari per il Nylon. "
                "Il riciclo meccanico è una tecnologia consolidata ma degrada la fibra: le sfilacciatrici spezzano "
                "il tessuto in fibre corte che richiedono l’aggiunta di materiale vergine. È un processo a basso impatto "
                "ambientale, ma porta inevitabilmente al downcycling e a prodotti di qualità inferiore come imbottiture"
                " o isolanti. "
            )

        # 2. Regola Assoluta: Nylon puro o senza elastan
        elif self.nylon > 0:
            return "🟢 Riciclo Chimico", (
                "Il riciclo chimico permette di ottenere fibre identiche alle vergini grazie a processi di depolimerizzazione "
                "o dissoluzione selettiva che superano i limiti del meccanico. È una tecnologia costosa ma altamente circolare: "
                "recupera i solventi in ciclo chiuso, riduce drasticamente acqua e impatto ambientale e diventa più conveniente "
                "man mano che aumentano i volumi di rifiuti trattati."
            )

            # 3. Gestione Contaminanti (Elastan) per i Triple Blend e altre mischie
        elif self.elastan > 0:
            if self.elastan < 6:
                return "🟢 Riciclo Chimico", (
                    "Il riciclo chimico permette di ottenere fibre identiche alle vergini grazie a processi di depolimerizzazione "
                    "o dissoluzione selettiva che superano i limiti del meccanico. È una tecnologia costosa ma altamente circolare: "
                    "recupera i solventi in ciclo chiuso, riduce drasticamente acqua e impatto ambientale e diventa più conveniente "
                    "man mano che aumentano i volumi di rifiuti trattati."
                )
            else:
                return "🔵 Riciclo Enzimatico", (
                    f"L'algoritmo rileva un blend con Elastan al {self.elastan}%. Poiché supera la soglia limite del 5%, "
                    "il riciclo chimico è bloccato per il rischio di degradazione dei solventi. Il sistema forza un processo "
                    "biotecnologico a enzimi per separare le fibre in modo selettivo."
                )

        # 4. Gestione Avanzata Mischie Lana/Acrilico
        elif self.lana > 0 or self.acrilico > 0:
            if self.lana > self.acrilico:
                return "🔵 Riciclo Enzimatico", (
                    "Avendo una forte maggioranza di fibra proteica (lana), il tessuto rischia il pilling. "
                    "Sfruttiamo enzimi (proteasi) che attaccano selettivamente solo le squame della lana, "
                    "levigandola. L'acrilico in minoranza non viene toccato e funge da 'scheletro' strutturale stabile.")
            elif self.acrilico > self.lana:
                return "🟢 Riciclo Chimico", (
                    "L'acrilico è maggioritario, accumula elettricità statica ed è inerte agli enzimi. "
                    "Il riciclo chimico permette di ottenere fibre identiche alle vergini grazie a processi di depolimerizzazione "
                    "o dissoluzione selettiva che superano i limiti del meccanico. È una tecnologia costosa ma altamente circolare: "
                    "recupera i solventi in ciclo chiuso, riduce drasticamente acqua e impatto ambientale e diventa più conveniente "
                    "man mano che aumentano i volumi di rifiuti trattati."
                )
            else:
                return "🔴 Riciclo Meccanico", (
                    "Il riciclo meccanico è una tecnologia consolidata ma degrada la fibra: le sfilacciatrici spezzano "
                    "il tessuto in fibre corte che richiedono l’aggiunta di materiale vergine. È un processo a basso impatto "
                    "ambientale, ma porta inevitabilmente al downcycling e a prodotti di qualità inferiore come imbottiture"
                    " o isolanti."
                    )

        # 5. Alta purezza Cellulosica: Riciclo Chimico per rigenerare Viscosa/Lyocell
        elif self.cotone > 60:
            return "🟢 Riciclo Chimico", (
                "Il riciclo chimico permette di ottenere fibre identiche alle vergini grazie a processi di depolimerizzazione "
                "o dissoluzione selettiva che superano i limiti del meccanico. È una tecnologia costosa ma altamente circolare: "
                "recupera i solventi in ciclo chiuso, riduce drasticamente acqua e impatto ambientale e diventa più conveniente "
                "man mano che aumentano i volumi di rifiuti trattati."
                )

        # 6. Blend Complessi (Es. Cotone-Poliestere equilibrati): Biotecnologie
        else:
            return "🔵 Riciclo Enzimatico", (
                "Il riciclo enzimatico usa biocatalizzatori che digeriscono selettivamente una fibra del blend, permettendo la "
                "separazione anche dei mix più complessi senza solventi tossici e con basse temperature. È la tecnologia più avanzata"
                "e sostenibile, ma oggi limitata dai costi elevati degli enzimi, gestita soprattutto da startup. "
                )


    # ======================================
    #           KPI AMBIENTALI
    # ======================================
    def kpi_ambientale(self):
        """Restituisce i 4 indicatori ambientali incrociando materiale e tecnologia LCA"""

        # 1. Identifichiamo la macro-categoria del materiale per la tabella
        if self.lana > 0 or self.acrilico > 0:
            cat_mat = "Lana e acrilico"
        elif self.nylon > 0 and self.elastan > 0:
            cat_mat = "Nylon-spandex"
        elif self.elastan > 0:
            cat_mat = "Triple Blend"
        else:
            cat_mat = "Policotone"

        # 2. Identifichiamo quale processo decisionale è stato assegnato dall'AI
        percorso, _ = self.calcola_riciclo()
        if "Meccanico" in percorso:
            tech = "Meccanico"
        elif "Chimico" in percorso:
            tech = "Chimico"
        else:
            tech = "Enzimatico"

        # 3. Database LCA con Indice di Affidabilità (Basato sul TRL - Technology Readiness Level)
        db_lca = {
            "Meccanico": {
                "Lana e acrilico": {"energia": "-70%", "co2": "-80%", "acqua": "-90%", "suolo": "-75%", "affidabilità": "5"},
                "Nylon-spandex": {"energia": "-40%", "co2": "-45%", "acqua": "-35%", "suolo": "0%", "affidabilità": "4"},
                "Policotone": {"energia": "-35%", "co2": "-40%", "acqua": "-60%", "suolo": "-35%", "affidabilità": "4"},
                "Triple Blend": {"energia": "-25%", "co2": "-25%", "acqua": "-40%", "suolo": "-20%", "affidabilità": "4"}
            },
            "Chimico": {
                "Lana e acrilico": {"energia": "-50%", "co2": "-65%", "acqua": "-80%", "suolo": "-70%", "affidabilità": "4"},
                "Nylon-spandex": {"energia": "-55%", "co2": "-70%", "acqua": "-50%", "suolo": "0%", "affidabilità": "3"},
                "Policotone": {"energia": "-50%", "co2": "-65%", "acqua": "-75%", "suolo": "-40%", "affidabilità": "4"},
                "Triple Blend": {"energia": "-45%", "co2": "-55%", "acqua": "-65%", "suolo": "-30%", "affidabilità": "4"}
            },
            "Enzimatico": {
                "Lana e acrilico": {"energia": "-60%", "co2": "-70%", "acqua": "-85%", "suolo": "-70%", "affidabilità": "3"},
                # Dati mancanti in letteratura
                "Nylon-spandex": {"energia": "N.D.", "co2": "N.D.", "acqua": "N.D.", "suolo": "N.D.", "affidabilità": "ND"},
                "Policotone": {"energia": "N.D.", "co2": "N.D.", "acqua": "N.D.", "suolo": "N.D.", "affidabilità": "ND"},
                "Triple Blend": {"energia": "N.D.", "co2": "N.D.", "acqua": "N.D.", "suolo": "N.D.", "affidabilità": "ND"}
            }
        }

        # 4. Estrazione dei valori precisi
        dati_selezionati = db_lca[tech][cat_mat]

        # 5. Formattazione dell'output
        return {
            "energia": dati_selezionati["energia"],
            "co2": dati_selezionati["co2"],
            "acqua": dati_selezionati["acqua"],
            "suolo": dati_selezionati["suolo"],
            "affidabilità": dati_selezionati["affidabilità"],  # Ora estrae il valore dinamico!
            "note_energia": "Risparmio di Specific Energy Consumption (SEC) rispetto alla produzione vergine.",
            "note_co2": "Fonti scientifiche: ivl.diva-portal.org | refashion.fr | sciencedirect.com",
            "note_acqua": "Risparmio idrico valutato sull'intero ciclo di vita (LCA).",
            "note_suolo": "Uso del suolo (Land Use). I sintetici puri (es. Nylon/Spandex) segnano 0% in quanto non necessitano di suolo agricolo alla radice."
        }

    # ======================================
    #           CALCOLO DISTANZA
    # ======================================

    def calcola_distanza_realistica(self, lat1, lon1, lat2, lon2, mezzo_scelto):

        # Raggio della Terra in chilometri
        R = 6371.0

        # Conversione delle coordinate da gradi a radianti
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        # Formula trigonometrica
        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2.0) ** 2

        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        distanza_linea_aria = R * c

        # 1. SE IL MEZZO È LA NAVE, APPLICHIAMO LA DEVIAZIONE MARITTIMA
        if mezzo_scelto.lower() == "nave":
            # Moltiplicatore logistico standard per rotte circumnavigate
            return distanza_linea_aria * 1.6

            # Se è camion o aereo, la linea d'aria (o autostradale) va bene
        elif mezzo_scelto.lower() == "camion":
            return distanza_linea_aria * 1.2  # coefficiente di tortuosità stradale

        elif mezzo_scelto.lower() == "treno":
            return distanza_linea_aria * 1.1  # coefficiente di tortuosità ferroviaria

        return distanza_linea_aria


    def get_partner_specializzati(self, lat_origine, lon_origine, is_green_list, paese_origine, tipo_trasporto="Camion", tecnica_suggerita=""):
        # 1. MIX ENERGETICO - CARBON INTENSITY (kg CO2 per kWh)
        # Valori calcolati in base alle percentuali di fonti fossili (Carbone, Gas, Petrolio)
        # vs fonti pulite (Idro, Eolico, Solare, Nucleare) fornite dai dati 2025.
        mix_energetico = {
            "Svezia": 0.02,  # Eccellente: quasi 100% Nucleare/Idro/Eolico
            "Svizzera": 0.03,  # Eccellente: 55% Idro, 27% Nucleare
            "Francia": 0.05,  # Ottimo: 67.5% Nucleare + Rinnovabili
            "Austria": 0.12,  # Buono: Forte Idro (47.5%) ma ancora 11.6% Gas e 2.2% Carbone
            "Spagna": 0.14,  # Buono: Molto Solare/Eolico, ma 20.6% Gas
            "Belgio": 0.17,  # Discreto: Nucleare/Eolico bilanciato da 18.2% Gas e 3% Carbone
            "Italia": 0.28,  # Critico: 38.4% Gas, 3.3% Fossili non spec., 15.7% Import
            "Olanda": 0.32,  # Critico: 36.4% Gas, 9.1% Carbone
            "Germania": 0.38  # Molto Critico: 20.7% Carbone, 16.3% Gas
        }

        # 2. FATTORI DI EMISSIONE TRASPORTO (kg CO2 per km per tonnellata)
        emissioni_trasporto = {
            "Treno": 0.02,  # Molto efficiente per lunghe distanze
            "Camion": 0.10,  # Standard su gomma
            "Nave": 0.025 #
        }
        fattore_trasporto = emissioni_trasporto.get(tipo_trasporto, 0.10)

        # 3. CONSUMO TECNOLOGIE (kWh per tonnellata)
        consumo_tecnologia = {
            "Raccolta e sorting": 50,
            "Meccanico": 1000,
            "Enzimatico": 1000,
            "Chimico": 1000  # Assegnato lo stesso consumo a tutte le tecniche per mancanza di dati affidabili!

        }

        # 4. DATABASE ATTORI COMPLETO (Ottimizzato contro i blocchi doganali nazionali)
        tutti_attori = [
            # --- NODI DI RACCOLTA E SORTING (Almeno 1 per nazione) ---
            {"nome": "TEXAID AG", "lat": 46.8647, "lon": 8.6472, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Svizzera"},
            {"nome": "I:CO (SOEX Group)", "lat": 53.6863, "lon": 10.2659, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Germania"},
            {"nome": "Boer Group Holland", "lat": 51.9641, "lon": 4.5939, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Olanda"},
            {"nome": "Comistra s.r.l.", "lat": 43.9115, "lon": 11.0264, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Italia"},
            {"nome": "Gebetex Tri Normandie", "lat": 49.1360, "lon": 1.3218, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Francia"},
            {"nome": "TEXLIMCA S.A.", "lat": 39.1437, "lon": -0.4410, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Spagna"},
            {"nome": "Öpula Rohstoff", "lat": 48.1869, "lon": 16.5405, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Austria"},
            {"nome": "Evadam", "lat": 50.9443, "lon": 3.1233, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Belgio"},
            {"nome": "SIPTEX Sysav (Malmö)", "lat": 55.6050, "lon": 13.0038, "cat": "Tutti", "tecnica": "Raccolta e sorting", "nazione": "Svezia"},

            # --- IMPIANTI DI RICICLO MECCANICO ---
            {"nome": "Manteco S.p.A.", "lat": 43.9168, "lon": 11.0205, "cat": "Lana", "tecnica": "Meccanico", "nazione": "Italia"},
            {"nome": "Marchi & Fildi", "lat": 45.5627, "lon": 8.0577, "cat": "Acrilico", "tecnica": "Meccanico", "nazione": "Italia"},
            {"nome": "Recover (Hilaturas)", "lat": 38.7153, "lon": -0.6586, "cat": "Cotone", "tecnica": "Meccanico", "nazione": "Spagna"},
            {"nome": "Renaissance Textile", "lat": 48.0642, "lon": -0.7486, "cat": "Policotone", "tecnica": "Meccanico", "nazione": "Francia"},
            {"nome": "Altex Textil", "lat": 52.2039, "lon": 7.0425, "cat": "Tutti", "tecnica": "Meccanico", "nazione": "Germania"},
            {"nome": "Resortecs", "lat": 50.8405, "lon": 4.3189, "cat": "TripleBlend", "tecnica": "Meccanico", "nazione": "Belgio"},
            {"nome": "Purfi", "lat": 50.8761, "lon": 3.4241, "cat": "TripleBlend", "tecnica": "Meccanico", "nazione": "Belgio"},
            {"nome": "Frankenhuis B.V.", "lat": 52.2130, "lon": 6.8900, "cat": "Tutti", "tecnica": "Meccanico", "nazione": "Olanda"},
            {"nome": "WKS Textilrecycling", "lat": 48.2082, "lon": 16.3738, "cat": "Tutti", "tecnica": "Meccanico", "nazione": "Austria"},
            {"nome": "Rester Nordic SE", "lat": 59.3293, "lon": 18.0686, "cat": "Tutti", "tecnica": "Meccanico", "nazione": "Svezia"},

            # --- IMPIANTI DI RICICLO CHIMICO ---
            {"nome": "Worn Again", "lat": 47.4938, "lon": 8.7115, "cat": "Policotone, Lana", "tecnica": "Chimico", "nazione": "Svizzera"},
            {"nome": "Eeden GmbH", "lat": 51.9689, "lon": 7.5956, "cat": "Policotone", "tecnica": "Chimico", "nazione": "Germania"},
            {"nome": "Phoenxt", "lat": 52.4821, "lon": 13.3551, "cat": "Poliestere", "tecnica": "Chimico", "nazione": "Germania"},
            {"nome": "Ioniqa", "lat": 51.4504, "lon": 5.4859, "cat": "Poliestere", "tecnica": "Chimico", "nazione": "Olanda"},
            {"nome": "CuRe Tech.", "lat": 52.7661, "lon": 6.9298, "cat": "Poliestere", "tecnica": "Chimico", "nazione": "Olanda"},
            {"nome": "RE&UP", "lat": 52.3812, "lon": 4.8519, "cat": "Policotone", "tecnica": "Chimico", "nazione": "Olanda"},
            {"nome": "Circulose", "lat": 62.3941, "lon": 17.3482, "cat": "Cotone", "tecnica": "Chimico", "nazione": "Svezia"},
            {"nome": "OnceMore", "lat": 56.1925, "lon": 14.7471, "cat": "Policotone", "tecnica": "Chimico", "nazione": "Svezia"},
            {"nome": "Aquafil S.p.A.", "lat": 45.9182, "lon": 10.8852, "cat": "Nylon", "tecnica": "Chimico", "nazione": "Italia"},
            {"nome": "Lenzing AG (REFIBRA)", "lat": 47.9772, "lon": 13.6219, "cat": "Cotone, Policotone", "tecnica": "Chimico", "nazione": "Austria"},
            {"nome": "AITEX Polymer Circularity", "lat": 38.6983, "lon": -0.4736, "cat": "Poliestere, Nylon", "tecnica": "Chimico", "nazione": "Spagna"},
            {"nome": "Loop Industries France", "lat": 49.4860, "lon": 0.5340, "cat": "Poliestere, Nylon", "tecnica": "Chimico", "nazione": "Francia"},
            {"nome": "Purfi Chemical Division", "lat": 50.8333, "lon": 3.4333, "cat": "Tutti", "tecnica": "Chimico", "nazione": "Belgio"},

            # --- IMPIANTI DI RICICLO ENZIMATICO ---
            {"nome": "Carbios", "lat": 45.7772, "lon": 3.0870, "cat": "Poliestere", "tecnica": "Enzimatico", "nazione": "Francia"},
        ]

        partner_idonei = []
        for a in tutti_attori:
            # A. Controllo Materiale: L'azienda tratta questo materiale o li tratta "Tutti"?
            materiale_ok = any(parola.lower() in self.nome.lower() for parola in a["cat"].split(", ")) or a[
                "cat"] == "Tutti"

            # B. Controllo Tecnica: L'azienda è un sorter (sempre necessario) OPPURE usa la tecnica suggerita?
            tecnica_ok = (a["tecnica"] == "Raccolta e sorting") or (a["tecnica"].lower() in tecnica_suggerita.lower())

            # C. Controllo Dogana (Green List): Se NON in Green List, la nazione dell'azienda deve coincidere con l'origine
            dogana_ok = True
            if not is_green_list:
                # Estraiamo le due nazioni, le mettiamo minuscole e togliamo gli spazi
                nazione_azienda = a.get("nazione", "").strip().lower()
                nazione_utente = paese_origine.strip().lower()

                # Se non sono identiche, blocchiamo l'azienda
                if nazione_azienda != nazione_utente:
                    dogana_ok = False

            # Se supera TUTTI i test (Materiale, Tecnica e Dogana), allora procediamo al calcolo ambientale
            if materiale_ok and tecnica_ok and dogana_ok:
                dist = self.calcola_distanza_realistica(lat_origine, lon_origine, a["lat"], a["lon"], tipo_trasporto)
                co2_trasporto = dist * fattore_trasporto

                energia_kwh = consumo_tecnologia.get(a["tecnica"],
                                                     1000)  # Assicurati che sia 1000 per l'ottimizzazione LCA
                co2_kwh = mix_energetico.get(a.get("nazione", "Germania"), 0.25)
                co2_processo = energia_kwh * co2_kwh

                co2_totale = co2_trasporto + co2_processo

                a["Distanza_km"] = dist
                a["co2_trasporto"] = round(co2_trasporto, 1)
                a["co2_processo"] = round(co2_processo, 1)
                a["co2_totale"] = round(co2_totale, 1)

                partner_idonei.append(a)

        partner_idonei.sort(key=lambda x: x["co2_totale"])
        return partner_idonei