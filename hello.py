import tkinter as tk

def show_output():
    output_label.config(text="こんにちは あっちゃん") 


root = tk.Tk()
root.title("Python 出力ウィンドウ")
root.geometry("300x200")


output_label = tk.Label(root, text="", font=("Arial", 14))
output_label.pack(pady=20)


show_button = tk.Button(root, text="メッセージを表示", command=show_output)
show_button.pack()


root.mainloop()
