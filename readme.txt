                                  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                                  ┃    ReadMe - HKYou Escape    ┃
                                  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Your friends are trapped inside various buildings in HKU by an anonymous villain! There are some weird locks,
perhaps we can rescue them by solving these locks! Find this confusing, huh? No worries, we got someone who 
just figured out how to solve the simplest lock. He(?) will teach you the basis with two tutorials.



-- LAUNCH GAME --

You should be getting this game in a zipped file, containing the MYSTERY...
Please make sure you have the following files & folder in order to run the game:

- folder    "map"
- folder    "kits"
- folder    "screen"
- file      "main.py"

    !!! PLEASE DO NOT CHANGE THE CONTENT INSIDE THE FOLDER !!!

To start the game, just simply run the "main.py" file.
In terminal, type command : "python main.py"

You may notice a game file "gamedata.json" being generated during the game. 
    
    !!! PLEASE DO NOT CHANGE ITS CONTENT !!!

You can reset your game stats by DELETING this file, the game will generate a new one for next run.





-- BASIC CONTROLS --

╔══════════════════════════╗  ╭── TARGET ──╮
║        ┌───┐┌───┐        ║  │            │
║        │ 5 ││ 0 │        ║  │    5 5     │
║        └───┘└───┘        ║  │    5 5     │
║  ╭────────────────────╮  ║  │            │
║  │┌───┐┏━━━┓┏━━━┓┌───┐│  ║  │            │
║  ││ 0 │┃ 0 ┃┃ 0 ┃│ 5 ││  ║  ├ MOVE COUNT ┤
║  │└───┘┗━━━┛┗━━━┛└───┘│  ║  │            │
║  ╰────────────────────╯  ║  │     0      │
║   ┌───┐┏━━━┓┏━━━┓┌───┐   ║  │            │
║   │ 0 │┃ 5 ┃┃ 0 ┃│ 0 │   ║  ╰────────────╯
║   └───┘┗━━━┛┗━━━┛└───┘   ║
║        ┌───┐┌───┐        ║
║        │ 0 ││ 5 │        ║
║        └───┘└───┘        ║
╚══════════════════════════╝

See this board? This is the lock you will be tackling.
Do you see the bolded grids in the center? They are called the "CORE".
For others unbolded grids, they are called "MARGINS".
To solve the lock, you will have to match the "CORE" with the "TARGET" displayed on the right of the board.

The board above is now in ROW mode, the round-cornered frame is selecting the first row with CORE grids.
You can rotate the row using LEFT and RIGHT ARROW keys, or select different rows with UP and DOWN ARROW keys.

╔══════════════════════════╗  ╭── TARGET ──╮
║       ╭─────╮            ║  │            │
║       │┌───┐│┌───┐       ║  │    6 6     │
║       ││ 6 │││ 6 │       ║  │    6 6     │
║       │└───┘│└───┘       ║  │            │
║  ┌───┐│┏━━━┓│┏━━━┓┌───┐  ║  │            │
║  │ 0 ││┃ 0 ┃│┃ 0 ┃│ 6 │  ║  ├ MOVE COUNT ┤
║  └───┘│┗━━━┛│┗━━━┛└───┘  ║  │            │
║  ┌───┐│┏━━━┓│┏━━━┓┌───┐  ║  │     0      │
║  │ 0 ││┃ 0 ┃│┃ 0 ┃│ 0 │  ║  │            │
║  └───┘│┗━━━┛│┗━━━┛└───┘  ║  ╰────────────╯
║       │┌───┐│┌───┐       ║
║       ││ 0 │││ 0 │       ║
║       │└───┘│└───┘       ║
║       ╰─────╯            ║
╚══════════════════════════╝

The board above is now in COLUMN mode, the round-cornered frame is selecting the first column with CORE grids.
You can rotate the column using UP and DOWN ARROW keys, or select different columns with LEFT and RIGHT ARROW keys.

To switch between these two modes, just simply hit SPACEBAR.

!!! PLEASE NOTE THAT

    You can select and rotate only the rows and columns in the CORE, 
    while those with only MARGIN grids cannot be move directly.

!!!

If you feels like you can solve this in smarter (fewer) moves, then hit 'R' to reset the whole board!
During the game (except tutorial), you can pause the game by hitting 'M'. Your progress will be save, you can 
come back and continue rescuing your friends later.




-- KEY BINDINGS --

< LOCK >
UP & DOWN ARROW    : Select rows (row mode) / Rotate column (column mode)
LEFT & RIGHT ARROW : Rotate row (row mode) / Select columns (column mode) 
SPACEBAR           : Switch between row mode and column mode
'R'                : Reset game board

< GENERAL >
UP & DOWN ARROW    : Scroll through items on menu
Enter/Return       : Select from menu
'M'                : Pause game menu
SPACEBAR           : Confirm pause game




-- IMPLEMENTATION DETAILS --

Please refer to the folder "explainer" for more details on implementation in various aspects:

- code_structure.txt        (code overview)
- matrix.txt                (nested data structure)      
- level_generation.txt      (randomness)
- input_handling.txt        (input handling)
- seed_saving.txt           (random seed)




-- CREDITS --

Edwin : Puzzle Designer & Developer (Game Logic) / Documentation
Hugo  : UI & Backend Developer (Game Screen & File Save) / Test & Debug
Navya : Trailer Producer / Story Prompt & Menu Designer
Nesta : Write "readme.txt" / Test & Debug / Demo Producer
Asset : Level Design / Demo Producer 
Jooh  : Test & Debug / Demo Voice Over & Producer




-- VIDEO LINKS --

Trailer:    https://youtu.be/-qydiMua_fE?si=tWIx2zmbL5t7LUPA
Demo Video: https://youtu.be/6HASMLPuk88?si=7QcO8DAYIbQxpyBd


