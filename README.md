# CSE4471
Idea & Plan:
Create a game where the player types out a paragraph while a keylogger logs their keystrokes. Every so often, the keylogger will drop a character that was entered or flip two adjacent characters. It is up to the player to correctly type the paragraph and fix any errors that the keylogger makes along the way, before their time is up. We plan on implementing this with Python and the Tkinter GUI interface. 

How it goes: A paragraph will pop up and the player will immediately start typing while the timer counts down. The keylogger will display what’s been typed, along with the errors it manufactures. Once the player is finished, they will hit the submit button, and their text will be evaluated for errors. The objective is to finish typing as soon as possible, but time will be added to the players score if any errors were present when they hit submit.

Feature ideas:
-Drop random characters from being logged
-Flip random adjacent characters
-User can enter a key 3 times in a row in order to disable the keylogger error functions for a couple seconds
-A random character (a-z) has a bug where you must hit that key twice for it to log the letter once (change up which letter it is for each game)
    -I.e. you must hit “aa” for “a” to show up
    -If you just hit “a”, nothing will be logged



How we’re splitting up the work:
	-GUI display and functionality (paragraph, keylogging text, button, score, etc.)
		-Rachel Bobango
	-Keylogger (functionality, adding in the errors, etc.)
		-Ian Coates, Nisarg Amin
	-Timing (countdown implementation, adding time penalties, etc.) 
		-Nina Yao
  -Comparison of the final text to the paragraph they were supposed to type (counting # of errors left)
		-Rachel Bobago
	

