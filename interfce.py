import OperatorsOptimization as op
import tkinter as tk
from tkinter import ttk
import threading

root = tk.Tk()

root.geometry("300x200")  # GenişlikxYükseklik
root.title("Hedef Silah Eşleme")
root.configure(bg="#d1d1d1")
root.resizable(False, False)
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()


custom_font = ("Helvetica", 16, "bold")

def Fire():
    a = op.OperatorsPool(int(entry.get()), int(entry2.get()))

    print("creat started")
    a.Create()

    progress_bar.place(x=50, y=115)
    for i in range(10):
        progress_bar['value'] = i * 10
        root.update_idletasks()
        a.Process()

    progress_bar['value'] = 100

    new_window2 = tk.Toplevel(root)
    new_window2.title("Hedef Silah Eşleme Sonuç")
    new_window2.geometry("500x500")
    new_window2.configure(bg="#d1d1d1")

    scrollbar = tk.Scrollbar(new_window2)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    count = 1
    listbox = tk.Listbox(new_window2, yscrollcommand=scrollbar.set, font = custom_font)
    for i in a.theBest[-1].theBestChromosome:
        if i == 0:
            listbox.insert(tk.END, (str(str(count) + ". hedefe silah atanmamalıdır \n")))
            count += 1
        else:
            listbox.insert(tk.END ,(str(str(count) + ". hedefe " + str(i) + ". silah atanmalıdır \n")))
            count += 1

    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    #----------------------------------------------------------------------------------------------------

    new_window = tk.Toplevel(root)
    new_window.title("Operatörlerin Optimum Değerleri")
    new_window.geometry("500x150")
    new_window.resizable(False, False)
    new_window2.configure(bg="#d1d1d1")

    label = tk.Label(new_window, text= "optimum pool size", font = custom_font)
    label.place(x= 0, y = 0)
    label = tk.Label(new_window, text= a.theBest[-1].Decimal()[0], font = custom_font)
    label.place(x= 300, y = 0)
    label = tk.Label(new_window, text= "optimum iteration", font = custom_font)
    label.place(x= 0, y = 25)
    label = tk.Label(new_window, text= a.theBest[-1].Decimal()[1], font = custom_font)
    label.place(x= 300, y = 25)
    label = tk.Label(new_window, text= "optimum mutation rate", font = custom_font)
    label.place(x= 0, y = 50)
    label = tk.Label(new_window, text= a.theBest[-1].Decimal()[2], font = custom_font)
    label.place(x= 300, y = 50)
    label = tk.Label(new_window, text= "optimum fitness value", font = custom_font)
    label.place(x= 0, y = 75)
    label = tk.Label(new_window, text= a.theBest[-1].fitness, font = custom_font)
    label.place(x= 300, y = 75)



def start_progress():
    # Yükleme çubuğunu başlat
    progress_bar['value'] = 0

    # Uzun süren işlemi bir iş parçacığında çalıştır
    threading.Thread(target=Fire).start()


style = ttk.Style(root)

# Yeni bir stil tanımla
style.element_create("custom.Horizontal.Progressbar.trough", "from", "clam")
style.element_create("custom.Horizontal.Progressbar.pbar", "from", "clam")

style.layout("custom.Horizontal.TProgressbar",
             [('custom.Horizontal.Progressbar.trough', {'children':
                [('custom.Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'})])

# Stil özelliklerini ayarla
style.configure("custom.Horizontal.TProgressbar",
                troughcolor='white',
                thickness=30,  # Çubuğun kalınlığı
                bordercolor='black',
                relief='solid',
                borderwidth=5,
                background='black')  # Kenarlık kalınlığı

progress_bar = ttk.Progressbar(root, style="custom.Horizontal.TProgressbar", orient='horizontal', length=200, mode='determinate')


style.element_create("custom.Entry.field", "from", "clam")
style.layout("custom.TEntry",
             [('custom.Entry.field', {'children': [('Entry.padding', {'children': [('Entry.textarea', {'sticky': 'nswe'})],
                                                             'sticky': 'nswe'})], 'sticky': 'nswe'})])

# Stil özelliklerini ayarla
style.configure("custom.TEntry",
                background="white",
                foreground="black",
                bordercolor="black",
                lightcolor="gray",
                darkcolor="gray",
                relief="solid",
                borderwidth=5)

entry = ttk.Entry(root, style="custom.TEntry")
entry.place(x = 150, y = 15)

entry2 = ttk.Entry(root, style="custom.TEntry")
entry2.place(x = 150, y = 65)

style.element_create("custom.Button.border", "from", "clam")
style.layout("custom.TButton",
             [('Button.border', {'children': [('Button.focus', {'children': [('Button.padding', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})])

# Stil özelliklerini ayarla
style.configure("custom.TButton",
                background="lightgray",
                foreground="black",
                bordercolor="black",
                relief="solid",
                borderwidth=5)

button = ttk.Button(root, style="custom.TButton" ,text="Füzeleri Ateşle", command=Fire, width = 14)

button.place(x = 100, y= 150)


label = tk.Label(root, text= "Silah Sayısı", bg="#d1d1d1" ,font = custom_font)
label.grid(column = 0, row = 0, padx = 0, pady = 10)
label = tk.Label(root, text=" Hedef Sayısı", bg="#d1d1d1", font = custom_font)
label.grid(column = 0, row = 1, padx = 0, pady = 10)



root.mainloop()
