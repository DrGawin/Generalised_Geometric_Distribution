# create a new window
import tkinter as tk

################
# Tooltip Class
################

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.font = ('Calibri', 12)

    def show_tip(self):
        if self.tip_window or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    tooltip = Tooltip(widget, text)
    widget.bind('<Enter>', lambda event: tooltip.show_tip())
    widget.bind('<Leave>', lambda event: tooltip.hide_tip())
###############

root = tk.Tk()
#root.iconbitmap('epsilon.ico')

# set the window title
root.title("Generalised Geometric Distribution Calculator")

# Set the size of the window
root.geometry("500x580")
root.resizable(False,False)

# Intro box
intro_title = tk.Label(root, text="  About:", font=('Calibri bold', 12), anchor="w")
intro_title.grid(row=0, column=0, columnspan=3, sticky="w")
intro_frame = tk.Frame(root, bg=root.cget('bg'))
intro_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky='w')
intro_text = tk.Text(intro_frame, width=60, height=13, wrap=tk.WORD, bg=root.cget('bg'), font=('Calibri', 12))
intro_text.tag_configure("center", justify='center')
intro_text.insert(tk.END, "Consider an experiment that can either succeed or fail. You run this experiment repeatedly until you get your first success. Each time you fail, the probability of failure decreases. In maths terms, this is a generalised version of the geometric distribution. This app computes the expectation of the number of experiements needed to obtain the first success, as well as the cost of running such experiment.\n\n The default values below consider experiments with initial failure chance at 50%. Each failure decreases the chance of failure by 50% (so it goes from 50% to 25%, then to 12.5%, etc.). The cost of each experiment is £30. The accuracy field takes values from 1 to 10000 with 10000 being the most accurate - leave this field at 10000 unless you run into performance issues.")
intro_text.tag_add("left", "1.0", "end")
intro_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#intro_frame.config(width=intro_text.winfo_reqwidth())

# Initial failure probability entry
label_ProbFail = tk.Label(root, text="Initial failure probability:")
label_ProbFail.grid(row=2, column=0, pady=(40, 0))
entry_ProbFail = tk.Entry(root)
entry_ProbFail.grid(row=2, column=1, pady=(40, 0))
entry_ProbFail.insert(0, "0.5")
ProbFail_Help = tk.Button(root, text="?", font=('Calibri bold', 11))
create_tooltip(ProbFail_Help, "Enter a decimal between 0 and 1. A value of 0 means the experiment will always succeed")
ProbFail_Help.grid(row=2, column=2, pady=(40, 0))

# Decrease in failure probability entry
label_ProbFailDec = tk.Label(root, text="Decrease in the failure probability per failure:")
label_ProbFailDec.grid(row=3, column=0)
entry_ProbFailDec = tk.Entry(root)
entry_ProbFailDec.grid(row=3, column=1)
entry_ProbFailDec.insert(0, "0.5")
ProbFailDec_Help = tk.Button(root, text="?", font=('Calibri bold', 11))
create_tooltip(ProbFailDec_Help, "Enter a decimal between 0 and 1. Note that a value of 0 turns the model into classical geometric distribution. A value of 1 means the second experiment will always be successful.")
ProbFailDec_Help.grid(row=3, column=2)

# Desired accuracy entry
label_Accuracy = tk.Label(root, text="Desired accuracy:")
label_Accuracy.grid(row=4, column=0)
entry_Accuracy = tk.Entry(root)
entry_Accuracy.grid(row=4, column=1)
entry_Accuracy.insert(0, "10000")
Accuracy_Help = tk.Button(root, text="?", font=('Calibri bold', 11))
create_tooltip(Accuracy_Help, "Accuracy is an integer between 1 and 10000. It is recommended to keep this at 10000, lower this if you run into performance issues")
Accuracy_Help.grid(row=4, column=2,)

# Desired cost entry
label_Cost = tk.Label(root, text="Cost per experiment:")
label_Cost.grid(row=5, column=0)
entry_Cost = tk.Entry(root)
entry_Cost.grid(row=5, column=1)
entry_Cost.insert(0, "30")
Cost_Help = tk.Button(root, text="?", font=('Calibri bold', 11))
create_tooltip(Cost_Help, "Type in any non-negative number no higher than 10000000000.")
Cost_Help.grid(row=5, column=2,)

##################################
# Entry reading and error checking
##################################
def calculate():
    try:
        cost = int(entry_Cost.get())
        if cost < 0 or cost>10000000000:
            label_error.config(text="Error: cost must be a non-negative number no higher than 10000000000.")
            return 0
        else:
            label_error.config(text="")
    except ValueError:
        label_error.config(text="Error: cost must be a non-negative number no higher than 10000000000.")
        return 0
    # n is the number of iterations (It is standard in maths to use n)
    try:
        n = int(entry_Accuracy.get())
        if n < 1 or n > 10000:
            label_error.config(text="Error: accuracy must be an integer between 1 and 10000.")
            return 0
        else:
            label_error.config(text="")

    except ValueError:
        label_error.config(text="Error: accuracy must be an integer between 1 and 10000.")
        return 0
    # fail_ini is the initial failure probability
    # succ is a list of size n such that succ[k] refers to the probability of a successful upgrade GIVEN that k fails had occured k times in a row
    succ = [0] * (n + 1)
    try:
        fail_ini = float(entry_ProbFail.get())
        succ[0] = 1 - fail_ini
        if fail_ini < 0 or fail_ini > 1:
            label_error.config(text="Error: failure probability must be a decimal between 0 and 1.")
            return 0
        else:
            label_error.config(text="")
    except ValueError:
            label_error.config(text="Error: failure probability must be a decimal between 0 and 1.")
            return 0
    # fail_dec is the decrease in failure probability per failure
    try:
        fail_dec = float(entry_ProbFailDec.get())
        if fail_dec < 0 or fail_dec > 1:
            label_error.config(text="Error: decrease in failure probability must be a decimal between 0 and 1.")
            return 0
        else:
            label_error.config(text="")
    except ValueError:
            label_error.config(text="Error: decrease in failure probability must be a decimal between 0 and 1.")
            return 0
    # Define the rest of succ
    for i in range(1, n + 1):
        succ[i] = 1 - fail_ini * (1 - fail_dec) ** i

    # Define the array fail[k] to be the probability of failing k times consecutively, only for k>=1.
    fail = [float(0)] * (n + 1)
    fail[1] = 1 - succ[0]
    for i in range(2, n + 1):
        fail[i] = (1 - succ[i - 1]) * fail[i - 1]

    # Define the array pmf[k] to be the probability failing k times and then succeed at the (k+1)th try.
    # In maths term, pmf[k] is the probability mass function of our random variable
    pmf = [float(0)] * (n + 1)
    pmf[0] = succ[0]
    for i in range(1, n + 1):
        pmf[i] = succ[i] * fail[i]

    # define the array E[k] to be an approx. value of the expected number of fails before succeeding for the first time.
    # the higher k is, the more accurate the approximation
    # Note that the approximation is always an underestimate, if k is large enough, then the error would be negligible.
    E = [float(0)] * (n + 1)
    E[0] = pmf[0]
    for i in range(1, n + 1):
        E[i] = E[i - 1] + (i + 1) * pmf[i]

    total_cost = cost * E[n]
    exp = E[n]

    label_result_exp.config(text="The expected number of tries is " + str(exp) + ".")
    label_result_cost.config(text="The expected total cost is " + str(total_cost) + ".")

# Debug code
#    for j in range(0, 4):
#        print(pmf[j])
#    print(total_cost)
#    return 0

###################

# Error printing
label_error = tk.Label(root)
label_error.grid(row=7, column=0, columnspan=3)
label_result_exp = tk.Label(root)
label_result_exp.grid(row=8, column=0, columnspan=3)
label_result_cost = tk.Label(root)
label_result_cost.grid(row=9, column=0, columnspan=3)

# create the calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# start the event loop
root.mainloop()
