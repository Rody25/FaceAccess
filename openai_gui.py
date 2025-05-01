import tkinter as tk
from tkinter import scrolledtext
from openai_assistant import ask_openai

def launch_openai_gui(name="Bruker"):
    language="no"
    theme="light"

    def send_prompt():
        prompt=entry.get()
        if prompt.strip():
            chat_area.insert(tk.END, f"{name}: {prompt}\n", "user")
            entry.delete(0, tk.END)
            try:
                response=ask_openai(prompt)
            except Exception as e:
                response=f"[FEIL]: {e}"
            chat_area.insert(tk.END, f"ChatGPT: {response}\n", "bot")
            chat_area.see(tk.END)

    def vis_forklaring(tekst):
        chat_area.delete("1.0", tk.END)
        chat_area.insert(tk.END, f"[Kategori]: {tekst}\n", "info")
        chat_area.see(tk.END)

    def bytt_tema():
        nonlocal theme
        theme="dark" if theme=="light" else "light"
        oppdater_tema()

    def bytt_språk():
        nonlocal language
        language="en" if language=="no" else "no"
        oppdater_språk()

    def oppdater_tema():
        farger={
            "light": {"bg":"#f5f5f5", "chat_bg": "#ffffff", "btn": "#1a73e8", "text": "#202124"},
            "dark": {"bg":"#202124", "chat_bg": "#303134", "btn": "#8ab4f8", "text": "#e8eaed"}
        }
        f=farger[theme]
        root.configure(bg=f["bg"])
        title.config(bg=f["bg"], fg=f["text"])
        chat_frame.config(bg=f["chat_bg"])
        chat_area.config(bg=f["chat_bg"], fg=f["text"])
        input_frame.config(bg=f["bg"])
        entry.config(bg="#ffffff", fg="#000000")
        send_button.config(bg=f["btn"], fg="white")
        category_frame.config(bg=f["bg"])
        tema_btn.config(bg="#dddddd" if theme=="light" else "#666666")
        språk_btn.config(bg="#dddddd" if theme=="light" else "#666666")
        tøm_btn.config(bg="#dddddd" if theme=="light" else "#666666")

    def oppdater_språk():
        if language=="no":
            title.config(text=f"Velkommen, {name}!")
            send_button.config(text="Send")
            språk_btn.config(text="Språk: Norsk")
            tøm_btn.config(text="Tøm chat")
        else:
            title.config(text=f"Welcome, {name}!")
            send_button.config(text="Send")
            språk_btn.config(text="Language: English")
            tøm_btn.config(text="Clear chat")

    def tøm_chat():
        chat_area.delete("1.0", tk.END)

    #GUI-en
    root=tk.Tk()
    root.title("FaceAccess – OpenAI GUI")
    root.geometry("1000x720")
    root.configure(bg="#f5f5f5")

    title=tk.Label(root, text=f"Velkommen, {name}!", font=("Helvetica", 22, "bold"))
    title.pack(pady=(10, 5))

    chat_frame=tk.Frame(root, bd=1, relief=tk.SOLID)
    chat_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    chat_area=scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Arial", 13))
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    chat_area.tag_config("user", foreground="#1a73e8", font=("Arial", 12, "bold"))
    chat_area.tag_config("bot", foreground="#34a853", font=("Arial", 12))
    chat_area.tag_config("info", foreground="#80868b", font=("Arial", 11, "italic"))

    input_frame=tk.Frame(root)
    input_frame.pack(padx=20, pady=(0, 10), fill=tk.X)

    entry=tk.Entry(input_frame, font=("Arial", 13))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    entry.focus()

    send_button=tk.Button(input_frame, text="Send", font=("Arial", 12, "bold"), command=send_prompt)
    send_button.pack(side=tk.LEFT)

    #Kontrollknappene
    control_frame=tk.Frame(root)
    control_frame.pack(pady=(0, 5))

    tema_btn=tk.Button(control_frame, text="Bytt tema", font=("Arial", 10), command=bytt_tema)
    tema_btn.pack(side=tk.LEFT, padx=10)

    språk_btn=tk.Button(control_frame, text="Språk: Norsk", font=("Arial", 10), command=bytt_språk)
    språk_btn.pack(side=tk.LEFT, padx=10)

    tøm_btn=tk.Button(control_frame, text="Tøm chat", font=("Arial", 10), command=tøm_chat)
    tøm_btn.pack(side=tk.LEFT, padx=10)

    #Kategorier
    category_frame=tk.Frame(root)
    category_frame.pack(padx=20, pady=(0, 20))

    categories=[
        {"label":"Geografi", "desc": {"no": "Lær om land og steder.", "en": "Learn about countries and places."}, "bg": "#cce5ff"},
        {"label":"Historie", "desc": {"no": "Historiske hendelser og epoker.", "en": "Historical events and periods."}, "bg": "#ffe5cc"},
        {"label":"Vitenskap", "desc": {"no": "Fysikk, kjemi, biologi.", "en": "Physics, chemistry, biology."}, "bg": "#d6f5d6"},
        {"label":"Litteratur", "desc": {"no": "Forfattere og bøker.", "en": "Authors and books."}, "bg": "#f2e6ff"},
        {"label":"Musikk", "desc": {"no": "Musikkstiler og artister.", "en": "Music styles and artists."}, "bg": "#fff0f5"},
        {"label":"Teknologi", "desc": {"no": "AI og datateknologi.", "en": "AI and digital tech."}, "bg": "#e6f0ff"}
    ]

    for index, cat in enumerate(categories):
        btn=tk.Button(
            category_frame,text=cat["label"], font=("Arial", 11, "bold"),
            bg=cat["bg"],fg="#202124", width=20, height=2,
            command=lambda t=cat["desc"]: vis_forklaring(t[language])
        )
        btn.grid(row=index // 3, column=index % 3, padx=10, pady=10)

    entry.bind("<Return>", lambda event: send_prompt())

    oppdater_tema()
    oppdater_språk()
    root.mainloop()
