**Booking seeker**  
My personal project to make search of options easier and faster. I like to invent such different automations and involve them into my routine.

It's just a yet another Python project. You should set up the PostgreSQL database and run main.ru.

Like this ``python main.py``

Before the first running you have to start database mirgrations using -m parameter: ``python main.py -m``

Project contains 4 applications:
- Scavenger, it collects the data from site and put raw data in the db
- Analyser, it make processing and filtering the data. All results are being stored in the datatbase.
- Notifier, telegram bot that tacke the data from db and send it to telegram user
- Raw fetch options saver, gets a raw url and transform it to set of fetch options that are supposed to be used by scavenger.
  - Library for event bus
