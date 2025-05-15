import pandas as pd 
import numpy as np
from typing import Tuple, Optional
from power_flow import PQBus, PVBus, PowerFlow, SlackBus


def read_data_ieee_cdf(path : str) -> Tuple[pd.DataFrame,pd.DataFrame] :

    lines = []
    with open(path,'+r') as f:
        lines=f.readlines()

    line_bus_size_split = str(lines[1]).split(' ')
    # TO DO: Fazer busca pelas linhas pela linha que começa com "BUS DATA FOLLOWS" 
    # e então aplicar nessa linha o comando abaixo subistituindo o indice fixo [3] pela linha encontrada
    # TO DO: Contar quantas linhas entre a linha começando por "BUS DATA FOLLOWS" e a proxima linha iniciando por "-999"
    last_bus_line = int([l.strip() for l in line_bus_size_split if l.strip()][3])+2
    bars_ = lines[2:last_bus_line]
    bars = []
    for b in bars_:
        bar = []
        bar.append(str(b[0:4]).strip()) # Columns  1- 4   Bus number (I) *
        bar.append(str(b[5:17]).strip()) # Columns  7-17   Name (A) (left justify) *
        bar.append(str(b[18:20]).strip()) # Columns 19-20   Load flow area number (I) Don't use zero! *
        bar.append(str(b[20:23]).strip()) # Columns 21-23   Loss zone number (I)
        bar.append(str(b[24:26]).strip()) # Columns 25-26   Type (I) *
        bar.append(str(b[27:33]).strip()) # Columns 28-33   Final voltage, p.u. (F) *
        bar.append(str(b[33:40]).strip()) # Columns 34-40   Final angle, degrees (F) *
        bar.append(str(b[41:49]).strip()) # Columns 41-49   Load MW (F) *
        bar.append(str(b[49:59]).strip()) # Columns 50-59   Load MVAR (F) *
        bar.append(str(b[59:67]).strip()) # Columns 60-67   Generation MW (F) *
        bar.append(str(b[67:75]).strip()) # Columns 68-75   Generation MVAR (F) *
        bar.append(str(b[76:83]).strip()) # Columns 77-83   Base KV (F)
        bar.append(str(b[84:90]).strip()) # Columns 85-90   Desired volts (pu) (F) (This is desired remote voltage if this bus is controlling another bus.
        bar.append(str(b[90:98]).strip()) # Columns 91-98   Maximum MVAR or voltage limit (F)
        bar.append(str(b[98:106]).strip()) # Columns 99-106  Minimum MVAR or voltage limit (F)
        bar.append(str(b[106:114]).strip()) # Columns 107-114 Shunt conductance G (per unit) (F) *
        bar.append(str(b[114:122]).strip()) # Columns 115-122 Shunt susceptance B (per unit) (F) *
        bar.append(str(b[123:127]).strip()) # Columns 124-127 Remote controlled bus number
        bars.append(bar)


    bars = pd.DataFrame(bars)
    bars.columns = ['Bus number','Name','Load flow area number','Loss zone number','Type','Final voltage','Final angle',
                    'Load MW','Load MVAR','Generation MW','Generation MVAR','Base KV','Desired volts (pu)','Maximum MVAR',
                    'Minimum MVAR','Shunt conductance G','Shunt susceptance B','Remote controlled bus number']


    # TO DO: Fazer busca pelas linhas pela linha que começa com "BRANCH DATA FOLLOWS" 
    # e então aplicar nessa linha o comando abaixo subistituindo o calcuo de indice pela linha encontrada
    # TO DO: Contar quantas linhas entre a linha começando por "BRANCH DATA FOLLOWS" e a proxima linha iniciando por "-999"
    line_lines_size_split =  str(lines[last_bus_line+1]).split(' ')
    last_line_line = [l.strip() for l in line_lines_size_split if l.strip()]
    last_line_line = int(last_line_line[3])+1
    lines_ = lines[(last_bus_line+2):(last_bus_line+last_line_line)]

    line_connects = []
    for l in lines_:
        ln_con = []
        ln_con.append(str(l[0:4]).strip()) # Columns  1- 4   Tap bus number (I) *
        ln_con.append(str(l[5:9]).strip()) # Columns  6- 9   Z bus number (I) *
        ln_con.append(str(l[10:12]).strip()) # Columns 11-12   Load flow area (I)
        ln_con.append(str(l[12:15]).strip()) # Columns 13-14   Loss zone (I)
        ln_con.append(str(l[16:17]).strip()) # Column  17      Circuit (I) * (Use 1 for single lines)
        ln_con.append(str(l[18:19]).strip()) # Column  19      Type (I) *
        ln_con.append(str(l[20:29]).strip()) # Columns 20-29   Branch resistance R, per unit (F) *
        ln_con.append(str(l[30:40]).strip()) # Columns 30-40   Branch reactance X, per unit (F) * No zero impedance lines
        ln_con.append(str(l[41:50]).strip()) # Columns 41-50   Line charging B, per unit (F) * (total line charging, +B)
        ln_con.append(str(l[51:55]).strip()) # Columns 51-55   Line MVA rating No 1 (I) Left justify!
        ln_con.append(str(l[57:61]).strip()) # Columns 57-61   Line MVA rating No 2 (I) Left justify!
        ln_con.append(str(l[63:67]).strip()) # Columns 63-67   Line MVA rating No 3 (I) Left justify!
        ln_con.append(str(l[69:72]).strip()) # Columns 69-72   Control bus number
        ln_con.append(str(l[73]).strip()) # Column  74      Side (I)
        ln_con.append(str(l[76:82]).strip()) # Columns 77-82   Transformer final turns ratio (F)
        ln_con.append(str(l[84:89]).strip()) # Columns 84-90   Transformer (phase shifter) final angle (F)
        ln_con.append(str(l[90:97]).strip()) # Columns 91-97   Minimum tap or phase shift (F)
        ln_con.append(str(l[97:104]).strip()) # Columns 98-104  Maximum tap or phase shift (F)
        ln_con.append(str(l[105:111]).strip()) # Columns 106-111 Step size (F)
        ln_con.append(str(l[112:117]).strip()) # Columns 113-119 Minimum voltage, MVAR or MW limit (F)
        ln_con.append(str(l[118:126]).strip()) # Columns 120-126 Maximum voltage, MVAR or MW limit (F)
        line_connects.append(ln_con)

    line_connects = pd.DataFrame(line_connects)
    line_connects.columns = ['Tap bus number','Z bus number','Load flow area','Loss zone','Circuit','Type','Branch resistance R','Branch reactance X',
                    'Line charging B','Line MVA rating No 1','Line MVA rating No 2','Line MVA rating No 3','Control bus number',
                    'Side','Transformer final turns ratio','Transformer (phase shifter) final angle','Minimum tap or phase shift',
                    'Maximum tap or phase shift','Step size','Minimum voltage','Maximum voltage']

    return bars, line_connects

if __name__ == "__main__":
    bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\14_Barras\\ieee14cdf.txt")
    print(bars.info())
    print(line_connects.info())
    bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\30_Barras\\ieee30cdf.txt")
    print(bars.info())
    print(line_connects.info())
    bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\57_Barras\\ieee57cdf.txt")
    print(bars.info())
    print(line_connects.info())
    bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\118_Barras\\ieee118cdf.txt")
    print(bars.info())
    print(line_connects.info())
    bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\300_Barras\\ieee300cdf.txt")
    print(bars.info())
    print(line_connects.info())