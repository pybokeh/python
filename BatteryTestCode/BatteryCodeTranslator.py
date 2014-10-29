# Convert a Hex value to Binary value
def getHex2Bin(hex_value):
    # This is a Python "dictionary" that shows the hex value and its corresponding binary value
    hex2bin_dict = {
"0":"00000000",
"1":"00000001",
"2":"00000010",
"3":"00000011",
"4":"00000100",
"5":"00000101",
"6":"00000110",
"7":"00000111",
"8":"00001000",
"9":"00001001",
"a":"00001010",
"b":"00001011",
"c":"00001100",
"d":"00001101",
"e":"00001110",
"f":"00001111",
"g":"00010000",
"h":"00010001",
"i":"0",
"j":"00010010",
"k":"00010011",
"l":"00010100",
"m":"00010101",
"n":"00010110",
"o":"0",
"p":"00010111",
"q":"00011000",
"r":"00011001",
"s":"00011010",
"t":"00011011",
"u":"00011100",
"v":"00011101",
"w":"00011110",
"x":"00011111",
"y":"0",
"z":"0",
"-":"0",
"10":"00010000",
"11":"00010001",
"12":"00010010",
"13":"00010011",
"14":"00010100",
"15":"00010101",
"16":"00010110",
"17":"00010111",
"18":"00011000",
"19":"00011001",
"1a":"00011010",
"1b":"00011011",
"1c":"00011100",
"1d":"00011101",
"1e":"00011110",
"1f":"00011111",
"20":"00100000",
"21":"00100001",
"22":"00100010",
"23":"00100011",
"24":"00100100",
"25":"00100101",
"26":"00100110",
"27":"00100111",
"28":"00101000",
"29":"00101001",
"2a":"00101010",
"2b":"00101011",
"2c":"00101100",
"2d":"00101101",
"2e":"00101110",
"2f":"00101111",
"30":"00110000",
"31":"00110001",
"32":"00110010",
"33":"00110011",
"34":"00110100",
"35":"00110101",
"36":"00110110",
"37":"00110111",
"38":"00111000",
"39":"00111001",
"3a":"00111010",
"3b":"00111011",
"3c":"00111100",
"3d":"00111101",
"3e":"00111110",
"3f":"00111111",
"40":"01000000",
"41":"01000001",
"42":"01000010",
"43":"01000011",
"44":"01000100",
"45":"01000101",
"46":"01000110",
"47":"01000111",
"48":"01001000",
"49":"01001001",
"4a":"01001010",
"4b":"01001011",
"4c":"01001100",
"4d":"01001101",
"4e":"01001110",
"4f":"01001111",
"50":"01010000",
"51":"01010001",
"52":"01010010",
"53":"01010011",
"54":"01010100",
"55":"01010101",
"56":"01010110",
"57":"01010111",
"58":"01011000",
"59":"01011001",
"5a":"01011010",
"5b":"01011011",
"5c":"01011100",
"5d":"01011101",
"5e":"01011110",
"5f":"01011111",
"60":"01100000",
"61":"01100001",
"62":"01100010",
"63":"01100011",
"64":"01100100",
"65":"01100101",
"66":"01100110",
"67":"01100111",
"68":"01101000",
"69":"01101001",
"6a":"01101010",
"6b":"01101011",
"6c":"01101100",
"6d":"01101101",
"6e":"01101110",
"6f":"01101111",
"70":"01110000",
"71":"01110001",
"72":"01110010",
"73":"01110011",
"74":"01110100",
"75":"01110101",
"76":"01110110",
"77":"01110111",
"78":"01111000",
"79":"01111001",
"7a":"01111010",
"7b":"01111011",
"7c":"01111100",
"7d":"01111101",
"7e":"01111110",
"7f":"01111111",
"80":"10000000",
"81":"10000001",
"82":"10000010",
"83":"10000011",
"84":"10000100",
"85":"10000101",
"86":"10000110",
"87":"10000111",
"88":"10001000",
"89":"10001001",
"8a":"10001010",
"8b":"10001011",
"8c":"10001100",
"8d":"10001101",
"8e":"10001110",
"8f":"10001111",
"90":"10010000",
"91":"10010001",
"92":"10010010",
"93":"10010011",
"94":"10010100",
"95":"10010101",
"96":"10010110",
"97":"10010111",
"98":"10011000",
"99":"10011001",
"9a":"10011010",
"9b":"10011011",
"9c":"10011100",
"9d":"10011101",
"9e":"10011110",
"9f":"10011111",
"a0":"10100000",
"a1":"10100001",
"a2":"10100010",
"a3":"10100011",
"a4":"10100100",
"a5":"10100101",
"a6":"10100110",
"a7":"10100111",
"a8":"10101000",
"a9":"10101001",
"aa":"10101010",
"ab":"10101011",
"ac":"10101100",
"ad":"10101101",
"ae":"10101110",
"af":"10101111",
"b0":"10110000",
"b1":"10110001",
"b2":"10110010",
"b3":"10110011",
"b4":"10110100",
"b5":"10110101",
"b6":"10110110",
"b7":"10110111",
"b8":"10111000",
"b9":"10111001",
"ba":"10111010",
"bb":"10111011",
"bc":"10111100",
"bd":"10111101",
"be":"10111110",
"bf":"10111111",
"c0":"11000000",
"c1":"11000001",
"c2":"11000010",
"c3":"11000011",
"c4":"11000100",
"c5":"11000101",
"c6":"11000110",
"c7":"11000111",
"c8":"11001000",
"c9":"11001001",
"ca":"11001010",
"cb":"11001011",
"cc":"11001100",
"cd":"11001101",
"ce":"11001110",
"cf":"11001111",
"d0":"11010000",
"d1":"11010001",
"d2":"11010010",
"d3":"11010011",
"d4":"11010100",
"d5":"11010101",
"d6":"11010110",
"d7":"11010111",
"d8":"11011000",
"d9":"11011001",
"da":"11011010",
"db":"11011011",
"dc":"11011100",
"dd":"11011101",
"de":"11011110",
"df":"11011111",
"e0":"11100000",
"e1":"11100001",
"e2":"11100010",
"e3":"11100011",
"e4":"11100100",
"e5":"11100101",
"e6":"11100110",
"e7":"11100111",
"e8":"11101000",
"e9":"11101001",
"ea":"11101010",
"eb":"11101011",
"ec":"11101100",
"ed":"11101101",
"ee":"11101110",
"ef":"11101111",
"f0":"11110000",
"f1":"11110001",
"f2":"11110010",
"f3":"11110011",
"f4":"11110100",
"f5":"11110101",
"f6":"11110110",
"f7":"11110111",
"f8":"11111000",
"f9":"11111001",
"fa":"11111010",
"fb":"11111011",
"fc":"11111100",
"fd":"11111101",
"fe":"11111110",
"ff":"11111111"}
    hex_value = hex_value.lower()  # convert any upper case input characters to lower case, otherwise there won't be a match!
    bin_value = hex2bin_dict[hex_value]
    return bin_value

# Below are Python "dictionaries" that convert the various battery code numeric attributes to their text equivalents
result_dict = {0:"Good Battery", 1:"Good - Recharge", 2:"Good - Recharge", 3:"Good", 4:"Replace Battery", 5:"Charge & Retest", 6:"Bad Cell - Replace"}

batt_type_dict = {0:"Lead Acid", 1:"Glass Mat", 2:"Group 31"}

test_type_dict = {0:"ED18 V1", 1:"ED18 V2", 2:"GR8 Dealer Inventory", 3:"GR8 Customer Vehicle"}

sw_vers_dict = {0:"Version 1", 1:"Version 2", 2:"Version 3", 3:"Version 4"}

# Convert a binary value to a decimal value
def getBin2Dec(bin_value):
    dec_value = int(bin_value,2)
    return dec_value     

# Concatenate or "glue" together the various parts of the battery code into the full 50-bit binary code
def batt2bin(test_code):
    try:
        if len(test_code) == 10:
            bin1=getHex2Bin(test_code[0:1])
            bin1=bin1[3:]
            bin2=getHex2Bin(test_code[1:2])
            bin2=bin2[3:]
            bin3=getHex2Bin(test_code[2:3])
            bin3=bin3[3:]
            bin4=getHex2Bin(test_code[3:4])
            bin4=bin4[3:]
            bin5=getHex2Bin(test_code[4:5])
            bin5=bin5[3:]
            bin6=getHex2Bin(test_code[5:6])
            bin6=bin6[3:]
            bin7=getHex2Bin(test_code[6:7])
            bin7=bin7[3:]
            bin8=getHex2Bin(test_code[7:8])
            bin8=bin8[3:]
            bin9=getHex2Bin(test_code[8:9])
            bin9=bin9[3:]
            bin10=getHex2Bin(test_code[9:10])
            bin10=bin10[3:]
            return bin1+bin2+bin3+bin4+bin5+bin6+bin7+bin8+bin9+bin10
        else:
            return "Concatenation Failed!"
    except KeyError:
        return "Not 10 digit code"

# Check to see if length of the binary battery code is 50
def check_bin_test_code(bin_code):
    if len(bin_code)==50:
        return "Good Test Code-It is 50 bits long"
    else:
        return "Bad Test Code"

# Get test type
def getTestType(bin_code):
    try:
        if check_bin_test_code(bin_code) != "Bad Test Code":
            return test_type_dict[getBin2Dec(bin_code[25:27])]
        else:
            return "Bad Test Code"
    except KeyError:
        return "Bad Test Code"

# Get version
def getVersion(bin_code):
    try:
        if check_bin_test_code(bin_code) != "Bad Test Code":
            return sw_vers_dict[getBin2Dec(bin_code[48:50])]
        else:
            return "Bad Test Code"
    except KeyError:
        return "Bad Test Code"    

# Get type
def getType(bin_code):
    try:
        if check_bin_test_code(bin_code) != "Bad Test Code":
            return batt_type_dict[getBin2Dec(bin_code[41:43])]
        else:
            return "Bad Test Code"
    except KeyError:
        return "Bad Test Code"
        
# Get voltage
def getVoltage(bin_code):
    if check_bin_test_code(bin_code) != "Bad Test Code":
        return getBin2Dec(bin_code[32:41]) / 10.00
    else:
        return -3

# Get result
def getResult(bin_code):
    try:
        if check_bin_test_code(bin_code) != "Bad Test Code":
            return result_dict[getBin2Dec(bin_code[13:16])]
        else:
            return "Bad Test Code"
    except KeyError:
        return "Bad Test Code"

# Get rating
def getRating(bin_code):
    if check_bin_test_code(bin_code) != "Bad Test Code":
       return getBin2Dec(bin_code[16:25]) * 5
    else:
        return -3

# Get battery capacity
def getCapacity(bin_code):
    if check_bin_test_code(bin_code) != "Bad Test Code":
       return getBin2Dec(bin_code[0:9]) * 5
    else:
        return -3

# Get temperature
def getTemp(bin_code):
    if check_bin_test_code(bin_code) != "Bad Test Code":
       return getBin2Dec(bin_code[27:32]) * 5 - 20
    else:
        return -3

# Get month
def getMonth(bin_code):
    if check_bin_test_code(bin_code) != "Bad Test Code":
       return getBin2Dec(bin_code[9:13])
    else:
        return -3

# Get day
def getDay(bin_code):
    if check_bin_test_code(bin_code) != "Bad Test Code":
       return getBin2Dec(bin_code[43:48])
    else:
        return -3

# Get battery SOC "State Of Charge"
def getSOC(bin_code, voltage):
    if check_bin_test_code(bin_code) != "Bad Test Code":
        if voltage >= 12.4:
            return "Charged"
        else:
            return "Discharged"
    else:
        return "Bad Test Code"
