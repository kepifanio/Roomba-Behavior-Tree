import time
import initiate
import random

SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
RUNNING = "RUNNING"

########################## BLACKBOARD SETUP ##########################
class Blackboard():
    def __init__(self, batteryLev, spot_cl, general_cl,
                dusty_spot, home_path, docked):
            self.batteryLev = batteryLev
            self.spot_cl = spot_cl
            self.general_cl = general_cl
            self.dusty_spot = dusty_spot
            self.home_path = home_path
            self.docked = docked


    def printBoard(self):
        print("\n")
        print("------BOARD VALUES------")
        print("Battery: ", self.batteryLev)
        print("Spot Clean: ", self.spot_cl)
        print("General Clean: ", self.general_cl)
        print("Dusty Spot: ", self.dusty_spot)
        print("Home Path: ", self.home_path)
        print("Docked: ", self.docked)
        print("\n\n")

# Initiate Blackboard values
batteryLev = random.randint(20,100)
spotClean = initiate.spot_clean()
generalClean = initiate.general_clean()
dustySpot = bool(random.randint(0,1))
blackboard = Blackboard(batteryLev, spotClean, generalClean,
                                      dustySpot, "", False);
blackboard.printBoard()

######################################################################


####################### NODE & COMPOSITE SETUP #######################
class Node:
    def __init__(self, label):
        self.label = label
        self.children = []
        self.status = None

class Composite(Node):
    pass

class Priority(Composite):
    def run(self):
        for child in self.children:
            child.run()
            if child.status == RUNNING:
                self.status = RUNNING
                return

class Sequence(Composite):
    def run(self):
        self.status = SUCCESS
        for child in self.children:
            child.run()
            if child.status == FAILURE:
                self.status = FAILURE
                return
            if child.status == RUNNING:
                self.status = RUNNING
                return

class Condition(Node):
    def __init__(self, label):
        super().__init__(label)

    def run(self):
        # SPOT_CLEAN LABEL
        if self.label == "spot_clean":
            if blackboard.spot_cl == True:
                self.status = SUCCESS
            else:
                self.status = FAILURE
                
        # BATTERY LABEL
        elif self.label == "battery_<_30":
            if blackboard.batteryLev < 30:
                print("Battery below 30%")
                self.status = SUCCESS
            else:
                self.status = FAILURE

        # DUSTY SPOT LABEL
        elif self.label == "dusty_spot":
            if blackboard.dusty_spot == True:
                print("Dusty spot found")
                self.status = SUCCESS
            else:
                self.status = FAILURE

        # GENERAL CLEANING LABEL
        elif self.label == "general_clean":
            if blackboard.general_cl == True:
                self.status = SUCCESS
            else:
                self.status = FAILURE

class Task(Node):
    def __init__(self, label, status):
        super().__init__(label)
        self.status = status

    def run(self):
        # FIND PATH HOME
        if self.label == "find_path":
            print("Finding path back home . . .")
            blackboard.home_path = "path home"
            print("Path found")

        # GO HOME
        elif self.label == "go_home":
            print("Returning home . . .")

        # DOCKING
        elif self.label == "docking":
            print("Docking . . . ")
            blackboard.docked = True

        # DO NOTHING
        elif self.label == "do_nothing":
            print("Doing nothing . . .")

        # SPOT CLEANING
        elif self.label == "spot_cleaning":
            print("Spot cleaning in progress . . .")

        # SPOT DONE
        elif self.label == "spot_done":
            print("Spot cleaning done")
            blackboard.spot_cl = False

        # GENERAL CLEANING
        elif self.label == "general_cleaning":
            print("General cleaning in progress . . .")

        # GENERAL CLEANING DONE
        elif self.label == "general_done":
            print("General cleaning done")
            blackboard.general_cl = False

        # Decrement battery level
        blackboard.batteryLev = blackboard.batteryLev - 1

class Selection(Composite):
    def run(self):
        self.status = FAILURE
        for child in self.children:
            child.run()
            if child.status == SUCCESS:
                self.status = SUCCESS
                return
            if child.status == RUNNING:
                self.status = RUNNING
                return

class Decorator(Node):
    pass

class Timer(Decorator):
    def __init__(self, label, time_val):
        super().__init__(label)
        time_label = self.label
        blackboard.time_label = time_val

    def run(self):
        time_label = self.label
        if blackboard.time_label != 0:
            self.children[0].run()
            self.status = RUNNING
            blackboard.time_label = blackboard.time_label - 1
        else:
            self.children[0].status = SUCCESS
            self.status = SUCCESS

        if self.label == "dusty_timer" and blackboard.time_label == 0:
            print("Dusty spot cleaned")
            blackboard.dusty_spot = False

class Negation(Decorator):
    def __init__(self, label):
        super().__init__(label)

    def run(self):
        self.children[0].run()
        currstatus = self.children[0].status
        if currstatus == FAILURE:
            self.status = SUCCESS
        elif currstatus == SUCCESS:
            self.status = FAILURE

class Until_Succesful(Decorator):
    def __init__(self, label):
        super().__init__(label)

    def run(self):
        currstatus = self.children[0].status
        if currstatus != SUCCESS:
            self.children[0].run()
            self.status = self.children[0].status
        else:
            self.status = SUCCESS



######################################################################


####################### MAKE TREE & RUN VACUUM #######################

# Function that runs the vacuum
def run(root):
    time_elapsed = 0

    while True:
        time_elapsed += 1
        print("Time Elapsed: ", time_elapsed)

        # Transition from docked to running after charging
        if blackboard.docked == True and blackboard.batteryLev == 100:
            blackboard.docked = False
            print("Charging complete. Undocking . . .")

        # Condition to continue charging
        if blackboard.docked == True and blackboard.batteryLev != 100:
            if blackboard.batteryLev % 10 == 0:
                blackboard.batteryLev += 10
            else:
                to_add = 10 - (blackboard.batteryLev % 10)
                blackboard.batteryLev += to_add
            print("Charging in progress . . . [Current Battery Level: ",
                                            blackboard.batteryLev, "%]")

        else:
            root.run()

        print("\n")
        time.sleep(1)

# Set up the tree
def make_tree():

    # Set up root composite (priority)
    root = Priority("root")

    # Set up battery composite (sequence)
    battery_seq = Sequence("battery_seq")
    charge = Condition("battery_<_30")
    find_path = Task("find_path", SUCCESS)
    go_home = Task("go_home", SUCCESS)
    docking = Task("docking", RUNNING)
    battery_seq.children = [charge, find_path, go_home, docking]

    # Set up cleaning composite(s)
    cleaning_sel = Selection("cleaning_selection")
    # ---spot cleaning---
    spot_seq = Sequence("spot_seq")
    spot_condit = Condition("spot_clean")
    spotcl_timer = Timer("spotcl_timer", 20)
    spot_cleaning = Task("spot_cleaning", RUNNING)
    spot_done = Task("spot_done", SUCCESS)
    spot_seq.children = [spot_condit, spotcl_timer, spot_done]
    spotcl_timer.children = [spot_cleaning]
    # ---general cleaning---
    dusty_timer = Timer("dusty_timer", 35)
    dusty_timer.children = [spot_cleaning]
    dusty_spot = Condition("dusty_spot")
    dusty_seq = Sequence("dusty_seq")
    dusty_seq.children = [dusty_spot, dusty_timer]
    general_cleaning = Task("general_cleaning", RUNNING)
    gen_selection = Selection("gen_selection")
    gen_selection.children = [dusty_seq, general_cleaning]
    gen_neg = Negation("gen_neg")
    gen_neg.children = [charge]
    gen_seq1 = Sequence("gen_seq1")
    gen_seq1.children = [gen_neg, gen_selection]
    until_succesful = Until_Succesful("until_succesful")
    until_succesful.children = [gen_seq1]
    general_done = Task("general_done", SUCCESS)
    gen_seq2 = Sequence("gen_seq2")
    gen_seq2.children = [until_succesful, general_done]
    general_clean = Condition("general_clean")
    general_sequence = Sequence("general_sequence")
    general_sequence.children = [general_clean, gen_seq2]
    cleaning_sel.children = [spot_seq, general_sequence]

    # Set up do nothing
    do_nothing = Task("do_nothing", SUCCESS)

    root.children = [battery_seq, cleaning_sel, do_nothing]

    return root

# Initiate running of vaccum
root = make_tree()
run(root)

######################################################################
