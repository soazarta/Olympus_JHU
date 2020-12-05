# Clue-Less Game

## Setup

Build and run the server
```
docker build -t clueless-server .
docker run -p 54321:54321 clueless-server
```

Run clients
```
python3 MainWindow.py
```

### Current Functionality

- **System Architecture**
    - Server subsystem with multiple clients
    - Two-way communication channels between server and clients

- **Implemented Logic**
    - Server setup
    - Multiple clients setup
    - Client choice of game character
    - Alternating between clients' turns (base code for gameplay)
    - Display of current game state on client and server
