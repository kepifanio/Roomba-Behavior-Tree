# Roomba-Behavior-Tree
Software implementation of a behavior tree for a Roomba-like vacuum.


Written by:      Katherine Epifanio (kepifa01)

Date:            2/23/21


Acknowledgements:

        https://towardsdatascience.com/designing-ai-agents-behaviors-with-behavior-trees-b28aa1c3cf8a

Purpose:

        Software implementation of a behavior tree for a
        Roomba-like vacuum. User input can indicate whether
        spot cleaning and/or general cleaning should be
        conducted.

Files:

        main.py - contains the majority of the source code,
                  responsible for setting up classes, global
                  variables, and running the vacuum

        initiate.py - responsible for reading in user preferences
                      regarding which tasks the vacuum should
                      complete

Compiling:

        python main.py

Usage:

        The command line only accepts "Y" or "N" in response to
        two prompts. Any other input is invalid and results
        in the program exiting.
