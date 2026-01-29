input_file = "input.txt"
output_file = "output.txt"

# reading input and making list of lines
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# the reason I am adding this block is to avoid breaking the code I wrote before explaining the input format.
lines = [line.strip() for line in lines]
lines.append("")

# function of transforming date and time tuple
def time_transformer(time_tuple):
    date = f"{time_tuple[0]}-{time_tuple[1]}-{time_tuple[2]}"
    time = f"{time_tuple[3]}:{time_tuple[4]}:{time_tuple[5]}"
    return [date, time]

# function of creating classified data dictionary which returns the dictionary
def classifier(line):
    temp_list = line.split()
    temp_time = temp_list[0].split("-")
    one_dict = {"time": (temp_time[0], temp_time[1], temp_time[2], temp_time[3], temp_time[4], temp_time[5]) , \
                                                            "user_id": int(temp_list[1]), \
                                                            "name": temp_list[2], \
                                                            "stock_name": temp_list[3], \
                                                            "order_type": temp_list[4], \
                                                            "share_num": int(temp_list[5]), \
                                                            "price": float(temp_list[6])}
    return one_dict

# creating list of dictionaries created by function
data_list = []
for i in range(len(lines) - 1):
    data_list.append(classifier(lines[i]))

# parsing orders by order_type to 2 lists
sell_list = []
buy_list = []
for i in data_list:
    d = i
    if d["order_type"] == "Sell":
        sell_list.append(i)
    else:
        buy_list.append(i)

# sorting by stock_name, price and user_id of sell list
sell_list = sorted(sell_list, key=lambda x: (x["time"], x["stock_name"], x["price"], x["user_id"]))
# sorting by stock_name, price and user_id of buy list
buy_list = sorted(buy_list, key=lambda x: (x["time"], x["stock_name"], -x["price"], x["user_id"]))

# first situtaion of sell and buy list with deepcopy
import copy
buy_list_first = copy.deepcopy(buy_list)
sell_list_first = copy.deepcopy(sell_list)

# list for orders
yazdır = []
# looking for matches
for buy in buy_list:
    for sell in sell_list:
        if buy["user_id"] != sell["user_id"] and buy["stock_name"] == sell["stock_name"] and buy["price"] >= sell["price"] and sell["share_num"] != 0:
            
            # determining how many shares are sold 
            shared = None
            if buy["share_num"] >= sell["share_num"]:
                shared = sell["share_num"]
            else:
                shared = buy["share_num"]

            # determining execution time and timestamp of earlier one between matched orders
            execution_time = None
            min_time = None
            if buy["time"] <= sell["time"]:
                execution_time = sell["time"]
                min_time = buy["time"]
            else:
                execution_time = buy["time"]
                min_time = sell["time"]
            execution_time_list = time_transformer(execution_time) 

            # appending results to "yazdır" list and updating sell and buy lists
            yazdır.append(f"{min_time} {buy["name"]} bought {shared} {buy["stock_name"]} for {sell["price"]} USD from {sell["name"]} on {execution_time_list[0]} at {execution_time_list[1]}")
            sell["share_num"] = sell["share_num"] - shared
            buy["share_num"] = buy["share_num"] - shared
            if buy["share_num"] == 0:
                break

# sorting by time order
sorted_yazdır = sorted(yazdır, key=lambda x: (x.split(" on ")[1], x[:37]))
results = [order[39:] for order in sorted_yazdır]

# printing and writing to output.txt
with open(output_file, "w", encoding="utf-8") as f:
    for result in results:
        print(result)
        f.write(result + "\n")

############### FUNCTIONS ############### FUNCTIONS ############### FUNCTIONS ###############
# total_executed_volume defining
def total_executed_volume(time):
    volume = 0
    
    for s in results:
        items = s.split()
        time_part_list = items[10:]
        time_part = time_part_list[0] + "-" + time_part_list[2].replace(":", "-")
        if time_part <= time:
            volume += int(items[2]) * float(items[5])
        else:
            break
        
    total = round(volume)
    return total

# executed_user_volume defining
def executed_user_volume(user_id, time):

    # finding owner of user_id
    for i in data_list:
        if i["user_id"] == user_id:
            name = i["name"]
            break
    
    volume = 0
    for s in results:
        items = s.split()
        time_part_list = items[10:]
        time_part = time_part_list[0] + "-" + time_part_list[2].replace(":", "-")
        if time_part <= time and (name == items[0] or name == items[8]):
            volume += int(items[2]) * float(items[5])

    total = round(volume)
    return total

# total_remaining_volume defining
def total_remaining_volume(time):

    # function of transforming time input to tuple 
    def time_tupler(time):
        time_list = time.split("-")
        time_tuple = tuple(item for item in time_list)
        return time_tuple
    time_tuple = time_tupler(time)

    # taking orders up to time for sell
    sell_list_trv = []

    import copy
    sell_list_second = copy.deepcopy(sell_list_first)
    
    for i in sell_list_second:
        if i["time"] <= time_tuple:
            sell_list_trv.append(i)

    # taking orders up to time for buy
    buy_list_trv = []

    import copy
    buy_list_second = copy.deepcopy(buy_list_first)
    
    for i in buy_list_second:
        if i["time"] <= time_tuple:
            buy_list_trv.append(i)

    # looking for matches
    for buy in buy_list_trv:
        for sell in sell_list_trv:
            if buy["user_id"] != sell["user_id"] and buy["stock_name"] == sell["stock_name"] and buy["price"] >= sell["price"] and sell["share_num"] != 0:
                
                # determining how many shares are sold 
                shared = None
                if buy["share_num"] >= sell["share_num"]:
                    shared = sell["share_num"]
                else:
                    shared = buy["share_num"]

                # determining execution time
                execution_time = None
                if buy["time"] <= sell["time"]:
                    execution_time = sell["time"]
                else:
                    execution_time = buy["time"]
                execution_time_list = time_transformer(execution_time) 

                # updating sell and buy lists
                sell["share_num"] = sell["share_num"] - shared
                buy["share_num"] = buy["share_num"] - shared
                if buy["share_num"] == 0:
                    break

    # calculating remaining volume 
    volume = 0 
    for i in buy_list_trv:
        volume += i["share_num"] * i["price"]
    for i in sell_list_trv:
        volume += i["share_num"] * i["price"]

    total = round(volume)
    return total

# remaining_user_volume defining
def remaining_user_volume(user_id, time):

    # function of transforming time input to tuple 
    def time_tupler(time):
        time_list = time.split("-")
        time_tuple = tuple(item for item in time_list)
        return time_tuple
    time_tuple = time_tupler(time)

    # taking orders up to time for sell
    sell_list_trv = []

    import copy
    sell_list_second = copy.deepcopy(sell_list_first)
    
    for i in sell_list_second:
        if i["time"] <= time_tuple:
            sell_list_trv.append(i)

    # taking orders up to time for buy
    buy_list_trv = []

    import copy
    buy_list_second = copy.deepcopy(buy_list_first)
    
    for i in buy_list_second:
        if i["time"] <= time_tuple:
            buy_list_trv.append(i)

    # looking for matches
    for buy in buy_list_trv:
        for sell in sell_list_trv:
            if buy["user_id"] != sell["user_id"] and buy["stock_name"] == sell["stock_name"] and buy["price"] >= sell["price"] and sell["share_num"] != 0:
                
                # determining how many shares are sold 
                shared = None
                if buy["share_num"] >= sell["share_num"]:
                    shared = sell["share_num"]
                else:
                    shared = buy["share_num"]

                # determining execution time
                execution_time = None
                if buy["time"] <= sell["time"]:
                    execution_time = sell["time"]
                else:
                    execution_time = buy["time"]
                execution_time_list = time_transformer(execution_time) 

                # updating sell and buy lists
                sell["share_num"] = sell["share_num"] - shared
                buy["share_num"] = buy["share_num"] - shared
                if buy["share_num"] == 0:
                    break

    # calculating remaining volume of user_id owner
    volume = 0 
    for i in buy_list_trv:
        if i["user_id"] == user_id:
            volume += i["share_num"] * i["price"]
    for i in sell_list_trv:
        if i["user_id"] == user_id:
            volume += i["share_num"] * i["price"]

    total = round(volume)
    return total

##################### TESTS OF FUNCTIONS ################### I tried to test in this way
#input4
#print(total_executed_volume('2024-11-18-16-21-18'))     #: 171897
#print(executed_user_volume(44, '2024-11-18-16-21-18'))  #: 87043
#print(total_remaining_volume('2024-11-18-16-21-18'))    #: 77424
#print(remaining_user_volume(44, '2024-11-18-16-21-18')) #: 23310
#print(total_executed_volume('2024-11-19-11-14-30'))     #: 252923
#print(total_remaining_volume('2024-11-19-11-14-30'))    #: 107550
#print(executed_user_volume(34, '2024-11-19-11-14-30'))  #: 125418
#print(remaining_user_volume(34, '2024-11-19-11-14-30')) #: 26149
#print(total_executed_volume('2024-11-18-10-17-15'))     #: 1860
#print(total_remaining_volume('2024-11-18-10-17-15'))    #: 6205
#print(executed_user_volume(47, '2024-11-18-10-17-15'))  #: 483
#print(remaining_user_volume(47, '2024-11-18-10-17-15')) #: 889

#input5
#print(total_executed_volume('2024-11-18-10-14-15'))     #: 1065
#print(total_remaining_volume('2024-11-18-10-14-15'))    #: 8644
#print(executed_user_volume(32, '2024-11-18-10-14-15'))  #: 0
#print(remaining_user_volume(32, '2024-11-18-10-14-15')) #: 1348
#print(total_executed_volume('2024-11-18-14-22-19'))     #: 236956
#print(total_remaining_volume('2024-11-18-14-22-19'))    #: 110245
#print(executed_user_volume(44, '2024-11-18-14-22-19'))  #: 119545
#print(remaining_user_volume(44, '2024-11-18-14-22-19')) #: 27242
#print(total_executed_volume('2024-11-18-17-57-30'))     #: 467625
#print(total_remaining_volume('2024-11-18-17-57-30'))    #: 151411
#print(executed_user_volume(47, '2024-11-18-17-57-30'))  #: 227742
#print(remaining_user_volume(47, '2024-11-18-17-57-30')) #: 43221