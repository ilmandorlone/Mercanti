# Game Board Application

## Descrizione del Programma

Questa applicazione è un gioco da tavolo basato su carte, dove i giocatori possono selezionare gettoni, riservare carte e acquistare carte utilizzando i gettoni accumulati. L'interfaccia utente è divisa in diverse sezioni: l'area dei giocatori, il tavolo di gioco e l'area del giocatore corrente.

## Struttura dei File

- `src/`
  - `components/`
    - `Card/`
      - `Card.jsx`
      - `Card.css`
    - `CardBack/`
      - `CardBack.jsx`
      - `CardBack.css`
    - `CardButtons/`
      - `CardButtons.jsx`
      - `CardButtons.css`
    - `CardRow/`
      - `CardRow.jsx`
      - `CardRow.css`
    - `GridLayout/`
      - `GridLayout.jsx`
      - `GridLayout.css`
    - `Player/`
      - `Player.jsx`
      - `Player.css`
    - `PlayerStatus/`
      - `PlayerStatus.jsx`
      - `PlayerStatus.css`
    - `SelectedTokens/`
      - `SelectedTokens.jsx`
      - `SelectedTokens.css`
    - `TokenList/`
      - `TokenList.jsx`
      - `TokenList.css`
  - `context/`
    - `CardContext.js`
  - `hooks/`
    - `usePlayers.js`
    - `useGameState.js`
  - `models/`
    - `CardModel.js`
  - `utils/`
    - `colors.js`

## Riassunto dei File

### `components/Card/Card.jsx`

Questo componente rappresenta una singola carta del gioco. Gestisce la visualizzazione dei costi dei gettoni, i pulsanti di azione (acquisto, riserva) e le interazioni dell'utente come la selezione della carta.

### `components/Card/Card.css`

Stili CSS per il componente `Card`, inclusi stili per la visualizzazione dei costi dei gettoni, i pulsanti di azione e l'aspetto generale della carta.

### `components/CardBack/CardBack.jsx`

Questo componente rappresenta il dorso di una carta coperta del mazzo. Mostra il livello della carta e include logica per la selezione della carta.

### `components/CardBack/CardBack.css`

Stili CSS per il componente `CardBack`, definendo l'aspetto del dorso della carta e la visualizzazione del livello.

### `components/CardButtons/CardButtons.jsx`

Questo componente gestisce i pulsanti di azione (acquisto, riserva) che compaiono quando una carta viene selezionata. I pulsanti sono posizionati al di fuori della carta selezionata.

### `components/CardButtons/CardButtons.css`

Stili CSS per il componente `CardButtons`, definendo l'aspetto dei pulsanti di azione e la loro posizione.

### `components/CardRow/CardRow.jsx`

Questo componente rappresenta una riga di carte sul tavolo di gioco. Include sia le carte scoperte che il dorso delle carte del mazzo.

### `components/CardRow/CardRow.css`

Stili CSS per il componente `CardRow`, definendo l'aspetto e la disposizione delle carte in una riga.

### `components/GridLayout/GridLayout.jsx`

Questo componente gestisce il layout principale dell'applicazione. Include l'area dei giocatori, il tavolo di gioco e l'area del giocatore corrente. Coordina anche le interazioni tra i diversi componenti.

### `components/GridLayout/GridLayout.css`

Stili CSS per il componente `GridLayout`, definendo il layout principale dell'applicazione e la disposizione delle diverse sezioni.

### `components/Player/Player.jsx`

Questo componente rappresenta un singolo giocatore nell'area dei giocatori. Visualizza il nome del giocatore e altre informazioni pertinenti.

### `components/Player/Player.css`

Stili CSS per il componente `Player`, definendo l'aspetto e il layout delle informazioni del giocatore.

### `components/PlayerStatus/PlayerStatus.jsx`

Questo componente visualizza lo stato corrente del giocatore, inclusi i gettoni e le carte possedute.

### `components/PlayerStatus/PlayerStatus.css`

Stili CSS per il componente `PlayerStatus`, definendo l'aspetto e la disposizione delle informazioni sullo stato del giocatore.

### `components/SelectedTokens/SelectedTokens.jsx`

Questo componente visualizza i gettoni selezionati dal giocatore per l'acquisto durante il turno corrente.

### `components/SelectedTokens/SelectedTokens.css`

Stili CSS per il componente `SelectedTokens`, definendo l'aspetto e la disposizione dei gettoni selezionati.

### `components/TokenList/TokenList.jsx`

Questo componente visualizza la lista dei gettoni disponibili per l'acquisto sul tavolo di gioco.

### `components/TokenList/TokenList.css`

Stili CSS per il componente `TokenList`, definendo l'aspetto e la disposizione dei gettoni disponibili.

### `context/CardContext.js`

Fornisce il contesto per la gestione dello stato delle carte selezionate e delle interazioni dell'utente con le carte.

### `hooks/usePlayers.js`

Un hook personalizzato per gestire lo stato e le informazioni dei giocatori.

### `hooks/useGameState.js`

Un hook personalizzato per gestire lo stato del gioco, inclusa la gestione dei gettoni e delle carte selezionate.

### `models/CardModel.js`

Definisce il modello di dati per una carta, inclusi attributi come l'id, il livello, il nome del colore e i costi dei gettoni.

### `utils/colors.js`

Contiene la mappatura dei colori per i gettoni e le carte, utilizzato per applicare i gradienti di colore e altre proprietà stilistiche.

---

Questo `README.md` fornisce una panoramica completa del programma, della struttura dei file e un riassunto dettagliato di ogni file. Puoi personalizzare ulteriormente le descrizioni e aggiungere dettagli specifici secondo necessità.
