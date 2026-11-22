# Lista materiali

Aggiornata il 22 novembre 2026. I materiali del progetto sono acquistati dalla scuola. Prezzi indicativi, salvo quelli dell'Arduino Store rilevati il 22/11/2026.

Stato: ✅ disponibile · 📦 ordinato / in arrivo · 🛒 nella richiesta d'acquisto · 🤔 da valutare

## Già disponibile

| Stato | Componente | Q.tà | Uso | Note |
|---|---|---|---|---|
| ✅ | Arduino UNO Q | 1 | Scheda principale | |
| ✅ | Hub USB-C | 1 | Monitor, tastiera, alimentazione | |
| ✅ | Modulino Distance (VL53L4CD) | 1 | Zona vicina | Portata ~1,2 m, cono 18° |
| ✅ | Modulino Vibro | 1 | Feedback tattile | |
| ✅ | Sensore ToF VL53L1X (modulo rosso «VL53LXX») | 3 | Piano di riserva senza camera: uno 22° in alto, uno dritto, uno 30° in basso | Del referente. Portata nominale 4 m, cono 27°. Pin da saldare; stesso indirizzo I²C dei Modulino Distance (serve il Modulino Hub o il pin SHUT) |
| ✅ | Webcam Logitech C270 | 1 | Riconoscimento oggetti (prototipo versione 3) | Non misura la profondità |
| ✅ | Power bank UGREEN Nexode 20.000 mAh 130 W | 1 | Prove in laboratorio | Del referente |
| 📦 | Modulino Movement (IMU) | 1 | Fermo / cammina; correzione dell'angolo del busto per il TF-Luna | |
| 📦 | Arduino UNO Q 4 GB, USB-C Hub 8 in 1, USB Camera, UNO Media Carrier | 1 cad. | Prove subito, senza attendere l'acquisto della scuola | Acquisto personale del referente del 22/11/2026 dall'Arduino Store: restano suoi e non sostituiscono righe della richiesta |

## Richiesta d'acquisto anno 1 (modulo scuola, versione finale del 22/11/2026)

Un prototipo completo. Stima complessiva circa 650–800 €. Da consegnare al DSGA (tipologia barrata: sussidi didattici, da verificare: UNO Q e camera potrebbero essere materiale inventariabile).

| Stato | n. | Componente | Produttore | Codice | Q.tà | Fornitore previsto | Uso |
|---|---|---|---|---|---|---|---|
| 🛒 | 1 | Arduino UNO Q 4 GB RAM / 32 GB eMMC | Arduino | ABX00173 | 1 | Arduino Store (bundle) | Scheda del prototipo |
| 🛒 | 2 | Camera di profondità con IA OAK-D Lite (fuoco fisso) | Luxonis | OAK-D-Lite-FF | 1 | Mouser / Robot-Italy | Sensore principale: ostacoli entro 2 m. Montata orizzontale sul petto |
| 🛒 | 3 | Modulino Distance (ToF 0–1,2 m) | Arduino | ABX00102 | 4 | Arduino Store | Zona vicina, puntati in alto e in basso |
| 🛒 | 4 | Modulino Hub (multiplexer I²C 8 canali) | Arduino | ABX00100 | 1 | Arduino Store | Più sensori con lo stesso indirizzo I²C |
| 🛒 | 5 | Modulino Movement (IMU 6 assi) | Arduino | ABX00101 | 1 | Arduino Store | Movimento della persona, angolo del busto |
| 🛒 | 6 | Modulino Vibro | Arduino | ABX00130 | 2 | Arduino Store | Vibrazione sinistra / destra |
| 🛒 | 7 | Modulino Buttons | Arduino | ABX00110 | 1 | Arduino Store | Comandi |
| 🛒 | 8 | Modulino Buzzer | Arduino | ABX00108 | 1 | Arduino Store | Avvisi sonori |
| 🛒 | 9 | Arduino USB-C Hub 8 in 1 (PD 65 W, USB-A 3.0, HDMI) | Arduino | TPX00241 | 1 | Arduino Store (bundle) | Alimenta UNO Q e camera |
| 🛒 | 10 | Power bank 20.000 mAh USB-C PD 87 W | Anker | A1383011 | 1 | RS Components | Alimentazione indossabile |
| 🛒 | 11 | Cavo USB-C/USB-C 24 pin (dati + 3 A), 0,5 m | a scelta | — | 2 | RS Components | |
| 🛒 | 12 | Kit cavi Qwiic assortiti | SparkFun | KIT-15081 | 1 | Mouser | Catena Qwiic dei sensori |
| 🛒 | 13 | LiDAR ToF TF-Luna 0,2–8 m | Benewake | TF-Luna | 1 | Robot-Italy | Gradini in discesa: puntato a terra davanti ai piedi |
| 🛒 | 14 | Cuffie Bluetooth a conduzione ossea | Creative (alt. Shokz OpenMove) | Outlier Free+ | 1 | — | Ritorno vocale tramite il Bluetooth 5.1 della UNO Q |
| 🛒 | 15 | Sensore ToF 4 m VL53L1X (Qwiic) | SparkFun | SEN-14722 | 3 | Mouser | Piano di riserva / conferma (+22°, dritto, −30°) |
| 🛒 | 16 | Cavo Qwiic – jumper femmina 4 pin, flessibile | SparkFun | CAB-17261 | 3 | Mouser | Collegare su Qwiic i 3 VL53L1X già disponibili |
| 🛒 | 17 | Arduino USB Camera | Arduino | TPX00246 | 1 | Arduino Store (bundle) | Piano B se la OAK-D Lite non funziona sulla UNO Q (supportata in App Lab) |
| 🛒 | 18 | Arduino USB-C Power Supply 45 W | Arduino | TPX00242 | 1 | Arduino Store (bundle) | Alimentazione in laboratorio |

**Ordine Arduino Store** (offerta Black Friday «Create your own bundle», prezzi IVA inclusa rilevati il 22/11/2026): UNO Q 4 GB 49,74 € (listino 82,90), USB-C Hub 10,14 €, USB Camera 21,00 €, Power Supply 45 W 10,14 €, 4 Modulino Distance 52,40 €, Modulino Hub 8,84 €, Modulino Movement 13,30 €, 2 Modulino Vibro 23,48 €, Modulino Buttons 8,50 €, Modulino Buzzer 7,30 € → **totale 204,84 €** (senza offerta circa 265,50 €). L'offerta scade presto: se la procedura (fattura elettronica PA, CIG) non permette di ordinare in tempo, le stesse righe si comprano a listino da RS o Mouser.

Altri prezzi indicativi, da verificare sui listini: OAK-D Lite circa 189–220 €; TF-Luna circa 36 €; cuffie a conduzione ossea di marca circa 65–100 €; SEN-14722 circa 30 $ l'uno e CAB-17261 circa 2 $ l'uno sul sito SparkFun.

La prova di compatibilità dell'audio Bluetooth si fa prima con le cuffie personali del referente: non serve attendere l'acquisto.

## Da valutare

| Stato | Componente | Q.tà | Uso | Note |
|---|---|---|---|---|
| 🤔 | Sensore ToF VL53L7CX 8×8 | 1 | Zona vicina a griglia, campo visivo largo | ~25 €, non acquistato |
| 🤔 | Sensore a ultrasuoni puntato dritto | 1 | Solo per le superfici in vetro | Proposto dopo il test simulato del 22/11: nessun sensore attuale vede la vetrata in tempo. Non deciso |

## Giubbino (reparto Moda) — anno 2

| Stato | Componente | Q.tà | Note |
|---|---|---|---|
| 🤔 | Gilet base tipo alta visibilità | da definire | |
| 🤔 | Tasche / supporti per sensori e scheda | da definire | Cartamodello a cura del reparto Moda |
| 🤔 | Supporti stampati in 3D per i sensori | da definire | Devono fissare gli angoli di puntamento dei sensori |

## Non più previsti

- Sensori a ultrasuoni HC-SR04 e ToF VL53L5CX: tolti dal progetto.
- Telecamera di profondità Orbbec Astra: sostituita dalla OAK-D Lite.

## Storico acquisti

| Data | Cosa | Stato |
|---|---|---|
| 2026-10 | Kit UNO Q + hub + Modulino Distance + Vibro | Arrivato |
| 2026-10 | Modulino Movement | Ordinato |
| 2026-11-21 | Richiesta d'acquisto anno 1 (13 righe + cuffie Bluetooth da aggiungere al modulo) | Compilata, da consegnare al DSGA |
| 2026-11-22 | Richiesta d'acquisto anno 1, versione finale a 18 righe (+ nota DSGA sull'offerta Arduino Store, 204,84 €) | Da consegnare al DSGA |
| 2026-11-22 | UNO Q 4 GB, USB-C Hub 8 in 1, USB Camera, UNO Media Carrier (Arduino Store) | Acquisto personale del referente, non della scuola |
