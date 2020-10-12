# tf2-automatic-profit
*The code was written in python3.8.2, but I guess it's working on python3.6 and above.*

### What it does?:
- **Calculates tf2-automatic bot profit** from its generated files.

### To get it running:
- **Set up** your **config_temp.py** file *(tools folder)*, **then rename** it **to config.py**. *(There are some information of the settings in the file itself.)*
- **Run** the **profit.py** file with ***python profit.py*** or with ***python***(whatever version you have, like 3.8) ***profit.py***

### You will see:
- **Profits** and \***trades, item by item**. *(if you set)*
- **Profits, day by day**.
- The 5 *(you can set this)* **most profitable items**.
- The 5 *(you can also set this)* **least profitable items**.
- **Estimated profit** and **profit/24 hours**.
- **Potential profit**. *(profit, if your bot sells all of its items)*

*\*trades: Accepted trades only, where the trade partner wasn't an admin and the items were traded for pure.*

### Notes:
- Key values may vary a bit, because of the 2 digit roundings.
- If you can't get it running you can contact me on discord. *(Martinovics#5979)*
- If the program crashes: (typically JSONDecodeError)
    - try to run it again (files might be corrupted) 
	- or you can send me your polldata and pricelist json files (on discord), so I can do further testing
- Also **let me know how accurate is this**.


*I hope you will find it useful.*
